# Strategy — The Worst App Idea Ever Pitched

## Exact deliverable

A source-bundle repo whose root `main.py` (Python 3.13, standard library only) writes exactly one
artifact: `/output/entry.txt`. The artifact is one sentence pitching the worst, most useless app
imaginable. It must be UTF-8, 1..240 characters inclusive, not only whitespace, with **no trailing
newline**, and final file mode **0644** (the grader refuses a mode-600 file). `/output` holds only
that artifact. `main.py` writes it atomically (temp file + `os.replace`), validates the bytes and
character count locally, and prints a short verification line. The repository keeps the makefun
freshness commit (`4c3e052`) and the MIT LICENSE commit (`d212d80`) untouched. No upload or
submission is performed in this session; only study, build, verify and commit.

## Scoring and the judge

The artifact goes through a validity gate, then a blind pairwise judge heat:

1. Gate: `/output/entry.txt` is UTF-8 text of 1 to 240 characters, not only whitespace. An invalid
   entry is never judged, ranks below every judged entry and takes no prize.
2. Judge: z-ai/glm-5.3-flash on OpenRouter, playing a deadpan product critic. Every pairing is
   judged twice, once in each A/B order. Margin 1..5 gives 0.6..1.0 of a call to the winner.
3. Heats: 3 Swiss rounds against other contenders and 3 fixed house texts, then a playoff among the
   top 10. Only contenders from the development board (top 500, or every valid entry while fewer)
   play in the final. Playoff finalists place above everyone else.
4. Ranking: Bradley-Terry win rate from final-heat games, higher is better. Top 8 places paid
   ($0.64 / $0.45 / $0.31 / $0.22 / $0.15 / $0.11 / $0.07 / $0.05). Byte-identical entries share a
   rate; exact ties go to playoff wins, then smaller text, then earlier receipt.
5. An entry needs the agent-session transcripts to be valid; that is handled by the session record,
   not by the artifact. The transcript gate checks that the anchor line quoted before the first
   counted write is present, that at least two assistant messages wrote the entrypoint, and that
   the entrypoint's lines are accounted for in the sessions.

## The judge's criteria, in the exact order it weighs them

1. Names a specific app and what it uselessly does, in one sentence pitched as the worst idea
   imaginable; a pitch that does not loses to any pitch of a useless app.
2. Makes the uselessness funny through absurd logic, deadpan confidence, or a perfect mismatch
   between a problem nobody has and the app that solves it.
3. Sounds like a real pitch, with a product name or a clear statement of what the app does and who
   it is for.
4. Uses the 240 characters well: one clean sentence, no padding, no second idea crowding it.
5. Leaves a vivid, specific picture of the app in the reader's head rather than a generic joke
   about apps.

The judge is told the best entries sound like a founder who means every word, that shock value for
its own sake does not count, and to decide on the first criterion where the two pitches differ.

## Hard caps

- Artifact: UTF-8, 1..240 characters, non-whitespace, no trailing newline, mode 0644.
- Runtime: 60 seconds wall, 512 MiB memory, 1 CPU, 64 PIDs, no network, no secrets.
- Everything the entry runs must live in the repository at the submitted commit.
- `/output` must contain only `entry.txt`.
- No vendor/ files exist in this repo; nothing in the kit is copied into it.

## Rival scan and chosen angle

I read the public leaderboard/feed (120 visible entry titles). The crowded angles are umbrellas,
puddles, refrigerators, naps/snooze alarms, socks, houseplants, toast, blinking, chat-verify gimmicks
and generic "worst app idea" placeholders. Copying any of those invites a near-duplicate rating and
gives the judge nothing fresh.

Chosen angle: a deadpan enterprise compliance app that certifies a body part attended a meeting.
The final pitch (221 characters, one sentence) is:

    SleeveCert: an enterprise app that photographs your elbow every 15 minutes during video calls, scores your cuff for meeting readiness, and bills $19/seat/month to email HR a signed PDF that HR deletes unopened by default.

Criterion-by-criterion fit:

1. Specific app (`SleeveCert`) and specific useless function (hourly elbow photos scored for
   "meeting readiness") in exactly one sentence.
2. Absurd logic: a compliance product whose proof is deleted unopened by its own recipient; the
   mismatch is a problem nobody has (was my cuff present?) met with an audit trail nobody reads.
3. Real pitch voice: named product, "enterprise app", per-seat price, Named recipient (HR), signed
   PDF — a founder could say it with a straight face.
4. 221 of 240 characters, one sentence, no padding and no second idea: every clause serves the
   single certification loop.
5. Vivid picture: a phone pointed at an elbow during a video call, a "meeting readiness" score, and
   a signed PDF landing in an HR trash folder.

## Concrete plan to maximize the score

1. Write the entrypoint once with a correct, simple artifact writer and validation.
2. Run it locally; inspect `/output/entry.txt` bytes, character count, trailing byte, mode and
   sha256; confirm `/output` has only that file.
3. Rewrite the *same* entrypoint in a separate step with the real compliance improvement: atomic
   temp-file creation in `/output`, explicit `chmod(0o644)` before `os.replace`, post-replace
   verification of mode/bytes/no trailing newline, and a clearer verification line on stdout.
4. Re-run it and repeat every check, including a second run to prove idempotence.
5. Commit all work after the second write on top of the existing anchor and LICENSE commits, and
   print the final commit sha. Do not submit or upload.
