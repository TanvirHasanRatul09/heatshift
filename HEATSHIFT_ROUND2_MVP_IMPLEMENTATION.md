# HEATSHIFT — Round 2 Modular MVP Implementation Plan

## 0. How to use this document

This is the implementation contract for the Round 2 prototype.

Implement **one module at a time**. After each module:

1. Run its verification checklist.
2. Show the changed files and result.
3. Stop and ask: **“Module X is complete. Should I start Module Y?”**
4. Do not start the next module without explicit user confirmation.

Do not implement optional modules early or expand the scope without confirmation.

## 1. Round 2 scope

HEATSHIFT is a local, presentation-ready decision-support prototype that transforms an unsafe work schedule during extreme heat into a safer feasible schedule using simulated workplace data.

The MVP demonstrates:

- workplace, zone, worker, task and shift input;
- an estimated heat-risk timeline;
- original versus recommended schedule;
- transparent heat-burden comparison;
- one working What-If scenario;
- a grounded explanation of the recommendation.
- a simulated multilingual message workflow using Bangla, English and Bangla-English mixed input.

This is not medical software, a live safety system, or a production deployment.

## 2. Technology stack — use correctly

### Required MVP stack

- **Frontend:** React, Vite, JavaScript or TypeScript, Tailwind CSS
- **Backend:** Python, FastAPI
- **Database:** SQLite for local persistence
- **Data access:** SQLAlchemy or SQLModel with a small seed dataset
- **Scheduling logic:** Python deterministic scoring and constraint checks
- **Communication:** REST/JSON between React and FastAPI
- **Deployment:** local machine only; no cloud dependency

### Responsibility of each technology

| Technology | Responsibility |
|---|---|
| React/Vite | Dashboard, schedule views, forms and What-If interaction |
| Tailwind CSS | Visual system and responsive layout |
| FastAPI | Validated API endpoints and orchestration |
| Python | Heat-burden calculation, validation and scheduling logic |
| SQLite | Store simulated workplaces, tasks, workers and scenarios |
| SQLAlchemy/SQLModel | Database models and queries |

Do not add Gemini, live weather APIs, IoT sensors, authentication, cloud deployment, voice, payroll, health tracking, multi-factory management or OR-Tools in the MVP. A live LLM is not required for this Round 2 prototype.

## 3. Repository structure

```text
heatshift/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/api.js
│   │   └── App.jsx
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── seed.py
│   │   ├── api/
│   │   └── services/
│   │       ├── heat_burden.py
│   │       └── scheduler.py
│   ├── requirements.txt
│   └── heatshift.db
├── README.md
└── .env.example
```

## 4. Module-by-module build plan

### Module 1 — Project foundation and local setup

**Goal:** Create runnable React and FastAPI applications.

**Tasks:**

- Initialise Vite React frontend.
- Initialise Python virtual environment and FastAPI backend.
- Add Tailwind CSS.
- Configure CORS for local frontend/backend communication.
- Add `GET /api/health` returning `{ "status": "ok" }`.
- Add a simple frontend status page.
- Add setup instructions to `README.md`.

**Verification:** Backend starts, `/api/health` works, frontend starts, and frontend displays backend status.

**Stop:** Do not create database models. Ask for confirmation before Module 2.

### Module 2 — SQLite database and dummy dataset

**Goal:** Persist the complete simulated Dhaka garment-factory scenario locally.

**Tasks:**

- Configure SQLite.
- Create models for workplace, zone, worker, task, heat condition and schedule item.
- Create a repeatable seed script and reset command.
- Add a read-only endpoint for the seeded scenario.
- Label every record as simulated/demo data.

**Seed scenario:** Simulated Dhaka garment factory, 9 AM–5 PM shift, 5 PM deadline, peak heat risk 12–3 PM, poorly ventilated loading area, one cooling/recovery area, and tasks for fabric-roll transfer, quality tagging, packing preparation, cooling/recovery and inventory update.

**Verification:** Database is created, reseeding is repeatable, API returns all scenario data, and no real personal/medical data exists.

**Stop:** Do not build scheduling logic. Ask for confirmation before Module 3.

### Module 3 — Heat-burden and risk service

**Goal:** Calculate an explainable estimated occupational heat-exposure score.

Use:

```text
heat burden = heat-risk score × task-intensity score × duration × zone-condition multiplier
```

Values: heat risk low 1, moderate 2, high 3, very high 4; intensity low 1, medium 2, high 3; ventilation good 0.8, normal 1.0, poor 1.3.

**Tasks:** Implement pure Python calculations, timeline lookup, per-task/total burden, risk labels, critical-window information and unit tests.

**Verification:** Same input gives the same score; original schedule shows high burden during 1–3 PM; API returns factors; label output as `Estimated occupational heat exposure — simulated comparison, not medical guidance.`

**Stop:** Do not optimize schedules. Ask for confirmation before Module 4.

### Module 4 — Constraint-based scheduling engine

**Goal:** Generate the lowest-burden valid schedule.

The engine must respect worker skill/availability, no overlapping assignments, task dependencies, cooling capacity, deadline, required recovery during high/very-high risk, and the rule that high-intensity work should not remain in a very-high-risk period when a safer valid slot exists.

**Tasks:** Generate schedule candidates in Python, reject invalid candidates, score valid candidates, return the best schedule and reasons, and add `POST /api/schedule/recommend`.

**Expected recommendation:** 9–11 fabric-roll transfer; 11–12 packing; 12–1 cooling/recovery; 1–3 quality tagging; 3–5 inventory update and remaining work.

**Verification:** Recommended schedule is valid, burden is lower, deadline is feasible, and no-safe-schedule works when transfer cannot move.

**Stop:** Do not build the full UI. Ask for confirmation before Module 5.

### Module 5 — FastAPI API layer

**Goal:** Expose only what the frontend needs.

Implement:

- `GET /api/health`
- `GET /api/demo/scenario`
- `GET /api/demo/original-schedule`
- `GET /api/demo/heat-timeline`
- `POST /api/schedule/recommend`
- `POST /api/schedule/what-if`

Add Pydantic schemas, validation, useful errors, local CORS and deterministic local responses. Verify all endpoints in Swagger at `/docs` without internet or API keys.

**Stop:** Ask for confirmation before Module 6.

### Module 6 — React dashboard and workflow

**Goal:** Visually demonstrate the decision workflow.

Build:

1. **Heat-Aware Operations Dashboard:** factory/date, heat timeline, critical window, original schedule, recommendation and burden comparison.
2. **Recommendation Explanation:** why the heavy task moved, based only on scenario data.
3. **What-If Simulator:** toggle `Fabric-roll transfer cannot be moved`; show no-safe-schedule and actions.
4. **How HEATSHIFT Works:** inputs → burden assessment → scheduling engine → safer feasible plan.

5. **Simulated Multilingual Input:** This is a required Round 2 presentation feature. Show exactly three fixed dummy messages with prewritten interpretations and replies. The three types are Bangla, English and Bangla-English mixed/Banglish. The reply must preserve the user's language style. This is a simulated presentation workflow, not live language processing.

Example:

```text
Input: দুপুরের heavy কাজটা সকালে করে দাও, তখন গরম কম থাকে।

Simulated interpretation:
Move the high-intensity fabric-roll transfer to an earlier lower-risk slot.

Simulated Bangla response:
Fabric-roll transfer কাজটি সকাল ৯–১১টার মধ্যে করা হবে। দুপুর ১২–১টা cooling/recovery break রাখা হয়েছে।

Example Banglish input:
Heavy kajta dupure na kore shokale kore dao, tokhon gorom kom thakbe.

Simulated Banglish response:
Heavy fabric-roll transfer kajta shokal 9–11 tar moddhe kora hobe. Dupur 12–1 ta cooling/recovery break rakha hoyeche.

Example English response:
Fabric-roll transfer has been moved to 9–11 AM. Cooling/recovery is scheduled from 12–1 PM.
```

Show the labels: `Simulated multilingual input demonstration — not live AI processing.` and `Reply language follows user input.`

### Required dummy message set

The frontend must include these three selectable demo messages. Do not require a language model or API to generate them.

| Type | Dummy user message | Dummy system reply |
|---|---|---|
| Bangla | `দুপুরের ভারী কাজটা সকালে করে দাও, তখন গরম কম থাকে।` | `Fabric-roll transfer কাজটি সকাল ৯–১১টার মধ্যে করা হবে। দুপুর ১২–১টা cooling/recovery break রাখা হয়েছে।` |
| English | `Move the heavy task to the morning because the afternoon heat is higher.` | `The fabric-roll transfer has been moved to 9–11 AM. Cooling/recovery is scheduled from 12–1 PM.` |
| Bangla-English mixed/Banglish | `Heavy kajta shokale kore dao, dupure gorom beshi thakbe.` | `Heavy fabric-roll transfer kajta shokal 9–11 tar moddhe kora hobe. Dupur 12–1 ta cooling/recovery break rakha hoyeche.` |

When a message is selected, display its prewritten reply and a structured interpretation. Add a visible badge: `Simulated multilingual demo`.

Keep scheduling logic in Python; the frontend only calls the API and renders results.

**Verification:** Dashboard loads, schedules differ clearly, What-If changes the result, and simulated-data labels are visible.

**Stop:** Ask for confirmation before Module 7.

### Module 7 — Demo polish and deck assets

**Goal:** Prepare screenshots and a reliable presentation demo.

- Use navy text, green safer state, orange recovery and red unsafe state.
- Make the before/after schedule the visual centrepiece.
- Add loading, empty and error states.
- Test a clean local start and capture screenshots.
- Add presenter notes for the demo flow.

Required disclaimer:

> HEATSHIFT is a decision-support prototype using simulated workplace data. It provides estimated occupational heat-exposure comparisons, not medical diagnosis or guaranteed safety. Human approval and validated occupational-safety guidance remain essential.

**Verification:** Demo works offline, screenshots are clear, and no unsupported real-world claims appear.

## 5. Optional post-MVP modules — do not start automatically

Only implement these after explicit approval: live Gemini/LLM processing for Bangla-English-Banglish input, live weather, indoor sensors, voice, authentication, PostgreSQL migration, OR-Tools, expert-validated heat models, pilot deployment and real worker feedback. The three dummy multilingual messages and their prewritten replies are required in the Round 2 MVP; only live language understanding is post-MVP.

## 6. Final acceptance checklist

- [ ] React/Vite frontend works.
- [ ] Python/FastAPI backend works.
- [ ] SQLite contains seeded dummy data.
- [ ] Heat-burden calculation is transparent and tested.
- [ ] Constraint-based recommendation works.
- [ ] Original versus recommended schedule is shown.
- [ ] What-If no-safe-schedule scenario works.
- [ ] Explanation is grounded in scenario inputs.
- [ ] All three dummy message types are shown: Bangla, English and Bangla-English mixed/Banglish.
- [ ] Each dummy input receives a reply in the same language style.
- [ ] No live API, sensor, cloud or LLM is required.
- [ ] Simulated data and non-medical status are clearly shown.
- [ ] The coding agent stopped after each module for confirmation.

## 7. Direct instruction to the coding agent

Read this file before coding. Start with **Module 1 only**. Do not implement later modules in the same turn. After verification, report:

```text
Module 1 complete.
Changed files: ...
Verification: ...
Known issues: ...
Should I start Module 2? (waiting for user confirmation)
```

Apply the same confirmation gate after every module.
