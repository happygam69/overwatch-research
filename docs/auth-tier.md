# The Battle.net authentication tower

`0x140bc86f0`–`0x140bda720`, chunks `0603`–`0611`, read at pass 67
(`ranges/0x140bb5e90-0x140bda720.md`, CODE_MAP ledger 85).

This is the client's whole account story: how Overwatch gets from "no session" to
"AUTHENTICATED, lobby connected". It is one object with one integer state and a pile
of web requests. Everything else in the band — the view/render belt in front of it,
the `[VC]` log helpers inside it — is either a neighbour or a passenger.

## The object

`AuthenticationSystem`, `0x768` bytes, constructed by `FUN_140bc7b30` and destroyed
by `FUN_140bc7f80` (its class-name page is `0x14386D4B0`). Its vtable is
`PTR_LAB_1430a2660`, with a second base at `PTR_FUN_142f87750`.

The fields worth knowing:

| offset | field |
|---|---|
| `+0x44` | **state**, 0…0x20 |
| `+0x50` | per-request timeout, **30000 ms** |
| `+0x58` | last retry tick (1 s gate; 10 s gate for the error display) |
| `+0x68…+0x74` | four status dwords copied from `_DAT_144188150…15c` on every reset |
| `+0x78` | the Battle.net connection object (`FUN_1423218c0`) |
| `+0xa0` | battleTag; `+0xc0` = has-display-name |
| `+0xc8/+0xd0/+0xd8` | the raw logon-complete blob `{ptr, size, cap}` |
| `+0xe0…+0x200` | ten strings, one per wait state |
| `+0x3b8`, `+0x3c8` | two 0xa8-byte row arrays (account-family / legal agreements) |
| `+0x400/+0x430` | result-row lock and the **0x90-byte result rows** |
| `+0x720` | a `0xde…` text tag for the current error, with its own 10 s expiry |
| `+0x754/+0x758` | report-enabled byte / the in-flight request |

Two clocks feed it. The state machine times out against a **double-precision
seconds** clock (`func_0x000141bbe1b0()+0x68 × _DAT_142f80e50`), while the retry
gates and the error display use the same source's `+0x40` field — server time and
local time [inference: two fields of one time object, which one is which is not
proven].

## The 33 states

Two static tables make the machine legible, both read out of the image with
`scripts/dumpva.py`:

* `0x14386dc30` — 33 pointers to the state-name pages (0…0x20). Every name is an
  XOR-8 page decoded in place, so a plain string search finds nothing.
* `0x14386db70` — 34 `u32`, **state → timeout-error message id** (0 = this state
  has no timeout text).

The ladder, in order: `WAIT_TO_START`, `FAILED`, `INITIAL_PSN_OR_XBL_AUTH`,
`RESOLVE_BNET`, `CONNECTING_TO_BNET`,
`WAITING_FOR_BNET_EXTERNAL_CHALLENGE`, `WAITING_FOR_PSN_OR_XBL_AUTH`,
`WAITING_FOR_ACCOUNT_FAMILY_AUTH`, `WAITING_FOR_BNET_JSON_AUTH_GET`,
`WAITING_FOR_USER_ACCOUNT_AND_PASSWORD`, `WAITING_FOR_BNET_CAPTCHA`,
`WAITING_FOR_USER_CAPTCHA`, `WAITING_FOR_USER_AUTHENTICATOR`,
`WAITING_FOR_USER_SMS_CHALLENGE`, `WAITING_FOR_USER_SMS_HEALUP`,
`WAITING_FOR_BNET_LEGAL`, `WAITING_FOR_USER_LEGAL`,
`WAITING_FOR_HEADLESS_ACCOUNT_CREATION`, `WAITING_FOR_ACCOUNT_LINKING_DATA`,
`WAITING_FOR_BRIDGE_ACCOUNT_LINKING_DATA`, `WAITING_FOR_ACCOUNT_LINK`,
`WAITING_FOR_BRIDGE_ACCOUNT_LINK`, `WAITING_FOR_ACCOUNT_LINKING_POLL_DATA`,
`WAITING_FOR_ACCOUNT_LINKING_POLL_DONE`,
`WAITING_FOR_BRIDGE_ACCOUNT_LINKING_POLL_DONE`,
`WAITING_FOR_BNET_LEGAL_CHALLENGE`, `WAITING_FOR_BNET_LEGAL_CHALLENGE_TEXT`,
`WAITING_FOR_BNET_LEGAL_SUBMIT`, `ATTEMPTING_LOGIN`, `VERIFY_CREDENTIAL`,
`AUTHENTICATED`, `AUTHENTICATED_LOBBY_CONNECTED`, `DISCONNECTED_LOBBY_CONNECTED`.

The `BNET_*` states are the client waiting on the server; the `USER_*` states are
the client waiting on a human. That distinction is exactly what
`FUN_140bcbcf0` encodes: states `{0,1,4,5,9,0xb,0xc,0xd,0xe,0x10,0x12…0x18,
0x1e,0x1f,0x20}` are never "timed out", because they are either terminal or
waiting on the player. Every other state compares the elapsed time against the
state's own deadline (`+0x48/+0x50`) and reports the tag from `0x14386db70`.

Once that table was read, every `state == N` test in the range decoded at once —
nine submits and handlers all keyed on the same enum, e.g. `__SubmitLogin`
requires 9, `__SubmitCaptcha` 0xb, `__SubmitAuthenticator` 0xc, `__SubmitLegal`
and `__SetLegal` 0x10.

## The loop

`FUN_140bc9d40` is the tick. It tears down a finished connection attempt, calls
the URL/legal/device helpers (`FUN_140bde9e0`, `FUN_140bde630`), and then: if the
state has a timeout text and the connection is alive, compare the elapsed time and
report; if the request has expired, report. Two independent retry timers sit on
top — a 1-second "still waiting" report and a 10-second re-ping — and the
post-auth states 0x1e/0x1f run a reconnect/watchdog loop with a 10-second guard.

Every submit ends with the same six-line idiom (evidence, six copies):

```
if (state != 1) {
    timedOut = timeoutTable[state] && FUN_140bcbcf0();
    if (state) setState(1);
    if (timedOut) vt+0xd8(v, 0, tag, state, msg);   // formatted
    else          vt+0xe0(v, tag, state, msg);      // plain
    vt+0x98(v, tag, state, msg);                    // post the event
    FUN_140bcb290(v);                               // reset
}
```

`tag` is the per-operation message id (`0x10067`…`0x100b1`), and `msg` is the
"Invalid state in X" page. So a failed submit is always: set state 1 (FAILED),
emit, post, reset.

## The web session

The client talks to Battle.net over plain HTTP requests handed to the **gate
service** (`_DAT_1439aef08 + 0xb2485ad1cf871d2c ^ 0x89d3e0b8c0994abf`), which owns
the curl-ish transport. `FUN_140bd44e0` allocates a request and refuses to make
more than **8 concurrent** ones. The response object carries the HTTP status at
`+0xc8` (200 = ok) and two string objects for body and error text.

The header contract is built by `FUN_140bcf740`: `Accept-Language`, `Device-Id`,
`Cookie: JSESSIONID=%s; web.id=%s`, one of four `Accept` values (json, plain,
markdown, json), `Content-type: application/json;charset=utf-8`, and
`User-Agent: Mozilla/4.0`. The product string is
`Overwatch/2.25.0.1.<revision>` (`FUN_140bd1de0`).

Request bodies are assembled by `FUN_140bd0dc0` (a formatted JSON builder) and the
login POST's fields are the pages `account_name`, `password`, `captcha`
(`0x14386eed0…ef40`). The HTTP method is a literal **3 = POST**, the request caps
are 0x1000 bytes with a 30 s timeout, and the login POST treats **200 or 400 as
"handled"** — Battle.net reports a rejected login as HTTP 400 with a JSON error body,
so a 400 still routes into the `authentication_state` parser.

The JSON layer is a small DOM: a node is `{ kind at +0x18, payload at +0x20 }`
with kind 2 = number, 3 = string, 4 = object, 5 = array, and
`FUN_14238cfa0(container, name)` is the member accessor used 37 times in this band.
The parser itself is a trio: `FUN_14238aa60` init, `FUN_14238d7b0(parser, copy)`
parse, `FUN_14238af60` destroy, with `FUN_14057fcf0` returning the root. On top of it sit nine
parsers, each named by its own error pages:

* `__ParseJsonAuthGet` (`FUN_140bd6430`) — the login form (`LOGIN_FORM`,
  `inputs`, `captcha_url`).
* `__ParseJsonAuthPost` (`FUN_140bd6c90`) — dispatches on `authentication_state`
  ∈ {`DONE`, `LOGIN`, `AUTHENTICATOR`, `LEGAL`} into:
  * `…_Done` (`FUN_140bd9250`, `login_ticket`),
  * `…_Login` (`FUN_140bd9f60`, `error_code`/`error_message`,
    `CAPTCHA_REQUIRED` + `url`, `ACCOUNT_BANNED`),
  * `…_Authenticator` (`FUN_140bd8940`, `next_url`, `authenticator_form`,
    `prompt`, `inputs`),
  * `…_Legal` (`FUN_140bd94b0`, `next_url`, `legal_form`, `agreements`).
* `__ParseLegalChallengeData` (`FUN_140bda720`) — `challenge`, `inputs`,
  `legal_agreements`.
* the three input extractors: `__ExtractJsonAuthGetInputs` (`FUN_140bcc970`, ids
  `account_name`/`password`/`captcha`/`log_in_submit`), `__ExtractAuthenticatorInputs`
  (`FUN_140bcc100`, ids `authenticator_input`/`remember_authenticator`/
  `authenticator_submit`) and `__ParseLegalSubmitJson` (`FUN_140bcd380`, `legal_submit`).
* device authorisation: `FUN_140bd7de0` (`device_code`, `user_code`,
  `verification_uri(_with_code)`, `polling_uri`, `interval_seconds`,
  `expires_in_seconds`) and `FUN_140bd7520` (poll: `id`,
  `expirationEpochMillis`, `links.status`, `links.start`).

The only URL literal in the band is
`https://identity.battle.net/bridge/v1` + `/delegation` (the account-link
delegation call). Everything else is composed from the connection object, so the
endpoint table is not in `.text` here.

## Errors

Two code spaces, both readable:

* **Battle.net status codes** map to messages in `FUN_140bd50b0`:
  0x35 `Account suspended`, 0x34 `Account banned`, 0x39 `Account locked`,
  0x4665 `SMS required`, 0x4666 `SMS already used`, 0x9c4e `Invalid NID`,
  0 `LogonComplete with no prometheus game accounts`.
* **Anything else** becomes `status + 0x2a | 0x20000` — a computable code space
  (the same formula appears in `__OnBnetConnected` and in the HTTP-status arm), so
  unknown failures are still typed, not stringly.

The account-family POST additionally carries a platform tag that is **`nexon`**
when the job's provider byte is 6 and `UNKNOWN` otherwise (`FUN_140bcadd0`,
pages `0x14386eb70`/`eb88`) — the Korean publisher path is the only one named.

The console/platform path is a separate decoder (`FUN_140bcb880`) over the
challenge protocol string: `psn://auth`, `xbl3://auth`, `nintendo://auth` → 1,
`externalChallenge=legal|healup|challenge|login` → 3/5/6/7, `device` → 4,
`headless` → 2.

## Passengers and neighbours

* **In front of the tower** (`0x140bb5e90`–`0x140bc60a0`) sits the **spectator /
  killcam orbit camera and the screen-marker overlay** — the client half pass 59
  predicted. Two families: a 0x2a0/0x2d0-byte **marker element** (world position,
  three basis rows, a phase/rate pair, a linger timer, three 0x20-byte curves; its
  entity-set differ `FUN_140bba700` keeps 8-byte `{id,flag,seen}` rows and compacts
  the unseen ones away; its draw builder `FUN_140bb8260` emits tag `0x10a1` with
  sub-tag `0x30e0` and one of three shapes 8/0x10/0x18), and a 0x340-byte **camera
  object** with a pivot + min/target/max orbit distance (`+0x490…+0x4d0`), a zoom
  accumulator, a mode enum at `+0x24c` (3 = blend, 4 = follow-with-zoom, 5 = free),
  two 3×4 matrices and **FOV 70.0°** (`0x3f9c61aa`). The two are joined through the
  **entity's camera blocks `+0x1260 {delta,dir}` and `+0x1310 {delta,a,b,c}`**:
  `FUN_140bc6240` writes them, `FUN_140bbed70` reads them back, `FUN_140bc52c0`
  pushes the result to `entity+0x10d0` for the scene emit. The band also holds one
  complete **open-addressing table** of the fifth hash family (`FUN_140bc2330` find,
  `FUN_140bc3880` grow).
* **Inside the tower** (`0x140bc72a0`–`0x140bc76f0`) live the `[VC]` voice client's
  tracker arms and their three expiry loggers — `==[VC] Login expired`,
  `==[VC] Join channel expired`, `==[VC] Leave channel expired`
  (`0x14386D428/D450/D480`). That closes the arm side of the pass-66 thread
  (T66-2); the tracker base constructor itself has no decompiled body.
* **After it** (chunk 0612, next pass) are the state setter `FUN_140bdd670`, the
  error emitter `FUN_140bdd2d0`, and the job bodies the submits hand their work to.

## What this tells us about the client

The account system is a browser-shaped web login, not a game-protocol login:
forms, captcha, authenticator, legal agreements, SMS challenges, device linking
and account linking are all *web pages and JSON*, and the state machine mostly
records which page the player is looking at. Only `CONNECTING_TO_BNET` /
`AUTHENTICATED` touch the game's own connection. The five `0xde…` text tags at
`+0x720` suggest the error surface is shared with the UI text namespace
(pass 56), i.e. auth errors are rendered from the same localized tag table as
everything else — an open thread, not a conclusion.

## What the second (full) read changed

The first pass over this band sampled the 21 decompilation windows; the second read every
line of all 209 entries and produced three corrections worth carrying:

1. **The windows are copies, not code.** Each giant's fabricated tail is a verbatim
   re-emission of a later function in the same range — `FUN_140bb9690` (declared 17 bytes,
   45 KB of text) is 42 stamps inside the auth object's destructor, `FUN_140bbbdc0` is 51
   stamps inside `__ParseLegalChallengeData`, `FUN_140bb72e0` (declared **one** byte) is 15
   stamps inside the view-scene emit. So the range's real code volume is its `size=` sum
   (114,805 B), and `size=1` headers mean the decompiler stopped early, not that the
   function is trivial.
2. **`0x14328cd40–cd4c` is not "the white row".** Dumped from the image it is
   `{0,0,0,0}`; the real white is `0x14328cd70–cd7c` (`{1,1,1,1}`) and `0x14328cd60–cd6c`
   is opaque black. The rows the quaternion bodies *add* (`0x14328cdc0/cdd0/cde0`) are the
   **identity basis**, so the additive term is the `1` of `1 − 2(y²+z²)`, not a tuning
   constant. Two of the five "Newton blocks" (`0x1430a1940`, `0x1430a1e70`) read as zero
   in the file image, i.e. they are initialised at runtime.
3. **The wire protocol is pinned**: method 3 = POST, caps 0x1000, 30 s timeout, the login
   POST accepts 200 *or* 400, `DAT_143bfeca0` is the "client live" latch every job tests,
   the account-family POST carries the provider tag `nexon` when its provider byte is 6,
   and the JSON node kinds are 2/3/4/5 = number/string/object/array.
