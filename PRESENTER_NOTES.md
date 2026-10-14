# HEATSHIFT Round 2 MVP presenter notes

1. Start the backend, seed the database, and open the frontend.
2. Point out the simulated Dhaka factory, 09:00–17:00 shift, and the 12:00–15:00 very-high-risk window.
3. Compare the original schedule with the recommended plan. Emphasize that fabric-roll transfer moves to 09:00–11:00 and recovery is scheduled at 12:00–13:00.
4. Use the What-If checkbox to lock the transfer. Show the `no-safe-schedule` result and the human-approval action.
5. Select Bangla, English, and Bangla-English mixed messages to demonstrate the fixed simulated communication workflow.
6. Close with the disclaimer: this is decision support using simulated data, not medical guidance or a guaranteed safety system.

## Demo reset

From `backend`, run `python -m app.seed` to restore the deterministic scenario.
