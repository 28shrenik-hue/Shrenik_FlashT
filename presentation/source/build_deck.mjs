import fs from "node:fs/promises";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const OUT = "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile_Capstone_Presentation_v1.pptx";
const ASSET = "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/presentation-build/assets";
const IMG = {};
for (const name of ["logo", "welcome", "goals", "lesson", "scenario", "deeper", "quiz", "team", "progress"]) {
  IMG[name] = new Uint8Array(await fs.readFile(`${ASSET}/${name}.png`));
}

const C = {
  bg: "#060B16",
  bg2: "#0B1327",
  panel: "#101C35",
  panel2: "#15294A",
  ink: "#F4F7FF",
  muted: "#A8B6D1",
  dim: "#7182A2",
  cyan: "#5CE1FF",
  blue: "#377DFF",
  violet: "#8A62FF",
  orange: "#FF9900",
  mint: "#68EDC6",
  line: "#2C4169",
};

const ppt = Presentation.create({ slideSize: { width: 1280, height: 720 } });

function rect(slide, x, y, w, h, fill, radius = 0, line = "none") {
  return slide.shapes.add({
    geometry: radius ? "roundRect" : "rect",
    position: { left: x, top: y, width: w, height: h },
    fill,
    line: { style: "solid", fill: line, width: line === "none" ? 0 : 1 },
    ...(radius ? { borderRadius: radius } : {}),
  });
}

function text(slide, value, x, y, w, h, size = 20, color = C.ink, bold = false, align = "left") {
  const box = slide.shapes.add({
    geometry: "textbox",
    position: { left: x, top: y, width: w, height: h },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  box.text = value;
  box.text.style = { fontSize: size, color, bold, alignment: align };
  return box;
}

function addImage(slide, name, x, y, w, h, fit = "contain", radius = 18) {
  rect(slide, x - 8, y - 8, w + 16, h + 16, C.panel, radius + 6, C.line).shadow = "shadow-lg";
  return slide.images.add({
    blob: IMG[name],
    contentType: "image/png",
    alt: `FlashTile ${name} screen`,
    fit,
    position: { left: x, top: y, width: w, height: h },
    geometry: "roundRect",
    borderRadius: radius,
  });
}

function chrome(slide, section, n) {
  slide.background.fill = C.bg;
  rect(slide, 0, 0, 14, 720, C.cyan);
  rect(slide, 14, 0, 6, 720, C.violet);
  text(slide, "FLASHTILE", 66, 32, 210, 26, 15, C.cyan, true);
  text(slide, section.toUpperCase(), 930, 34, 270, 24, 12, C.dim, true, "right");
  text(slide, `Knowledge that finds you.   ${String(n).padStart(2, "0")}`, 66, 680, 1134, 20, 11, C.dim, false, "right");
}

function title(slide, heading, sub = "", headingSize = 38, subY = 160) {
  text(slide, heading, 66, 84, 1134, 60, headingSize, C.ink, true);
  if (sub) text(slide, sub, 68, subY, 1050, 44, 19, C.muted, false);
}

function note(slide, presenter, talking, sources) {
  slide.speakerNotes.textFrame.setText(
    `Suggested presenter: ${presenter}\n\n${talking}\n\n[Sources]\n${sources.map((s) => `- ${s}`).join("\n")}\n[/Sources]`
  );
}

function metric(slide, value, label, x, y, color, width = 210) {
  text(slide, value, x, y, width, 76, 50, color, true);
  text(slide, label.toUpperCase(), x, y + 74, width, 30, 13, C.muted, true);
}

// 1 — Title
{
  const s = ppt.slides.add();
  s.background.fill = C.bg;
  rect(s, 0, 0, 18, 720, C.cyan);
  rect(s, 18, 0, 7, 720, C.violet);
  text(s, "FLASHTILE", 76, 72, 300, 34, 18, C.cyan, true);
  text(s, "Knowledge that\nfinds you.", 76, 180, 620, 156, 58, C.ink, true);
  text(s, "A tile-first enterprise learning companion\nfor continuous growth in the flow of work.", 80, 365, 570, 90, 24, C.muted, false);
  rect(s, 78, 500, 260, 4, C.orange);
  text(s, "ENTERPRISE LEARNING CAPSTONE", 80, 525, 410, 30, 14, C.orange, true);
  s.images.add({ blob: IMG.logo, contentType: "image/png", alt: "FlashTile 3D liquid-glass logo", fit: "contain", position: { left: 770, top: 95, width: 400, height: 500 } });
  text(s, "Tran, Victoria  •  Edupuganti, Kranthima  •  Griffin, Trey\nNeel, Jeffrey  •  Talley, Kyle  •  Patel, Shrenik", 78, 620, 870, 50, 15, C.dim, false);
  note(s, "Patel, Shrenik", "Open with the promise: FlashTile brings learning to employees instead of asking employees to leave their workflow to find it.", [
    `${ASSET}/logo.png`,
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/docs/Vision.md",
  ]);
}

// 2 — Problem
{
  const s = ppt.slides.add(); chrome(s, "The opportunity", 2);
  title(s, "Learning loses when it competes with the workday.", "The intent to grow is real. The friction is where, when, and how learning begins.");
  text(s, "01", 88, 242, 80, 55, 42, C.orange, true);
  text(s, "Another destination", 180, 238, 400, 44, 26, C.ink, true);
  text(s, "Traditional portals ask employees to stop, switch context, and search before learning can start.", 180, 284, 820, 54, 18, C.muted);
  rect(s, 88, 356, 1020, 1, C.line);
  text(s, "02", 88, 390, 80, 55, 42, C.violet, true);
  text(s, "Too much at once", 180, 386, 400, 44, 26, C.ink, true);
  text(s, "Long modules are difficult to fit into a full calendar—and easy to postpone.", 180, 432, 820, 54, 18, C.muted);
  rect(s, 88, 504, 1020, 1, C.line);
  text(s, "03", 88, 538, 80, 55, 42, C.cyan, true);
  text(s, "Weak daily momentum", 180, 534, 430, 44, 26, C.ink, true);
  text(s, "Without a small next step, progress becomes invisible and consistency fades.", 180, 580, 820, 54, 18, C.muted);
  note(s, "Patel, Shrenik", "Frame the problem without criticizing existing learning platforms. The opportunity is to complement them with a lightweight daily entry point.", [
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/docs/Proposal.md",
  ]);
}

// 3 — Solution
{
  const s = ppt.slides.add(); chrome(s, "The solution", 3);
  title(s, "FlashTile turns learning into a visible next step.", "A compact, always-on-top tile keeps development present without becoming another full-screen application.");
  addImage(s, "welcome", 842, 210, 261, 440);
  text(s, "It arrives where work happens.", 86, 236, 620, 52, 30, C.ink, true);
  text(s, "A focused tile stays at the edge of the desktop and opens with purpose—not clutter.", 88, 302, 590, 72, 20, C.muted);
  rect(s, 88, 410, 520, 3, C.cyan);
  text(s, "PERSONALIZED", 88, 440, 200, 26, 14, C.cyan, true);
  text(s, "Choose a learning goal.", 88, 474, 520, 34, 23, C.ink, true);
  text(s, "PRACTICAL", 88, 532, 200, 26, 14, C.orange, true);
  text(s, "Learn through realistic scenarios.", 88, 566, 560, 34, 23, C.ink, true);
  note(s, "Tran, Victoria", "Demonstrate the fixed tile size and emphasize that the product deliberately avoids a dashboard or full-screen shell.", [
    `${ASSET}/welcome.png`,
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/README.md",
  ]);
}

// 4 — Experience flow
{
  const s = ppt.slides.add(); chrome(s, "The experience", 4);
  title(s, "One continuous loop converts intent into progress.", "Every launch follows the same clear path; every completion creates the next learning moment.");
  const xs = [76, 306, 536, 766, 996];
  const labels = ["WELCOME", "CHOOSE GOAL", "LEARN", "CHECK", "PROGRESS"];
  const detail = ["Understand the promise", "Select one category", "Explore one concept", "Apply it in context", "Earn XP and recall"];
  for (let i = 0; i < 4; i++) {
    s.shapes.add({ geometry: "rightArrow", position: { left: xs[i] + 164, top: 330, width: 64, height: 38 }, fill: C.line, line: { style: "solid", fill: "none", width: 0 } });
  }
  for (let i = 0; i < 5; i++) {
    const color = [C.cyan, C.violet, C.orange, C.mint, C.blue][i];
    rect(s, xs[i], 272, 168, 158, C.panel, 24, color);
    text(s, String(i + 1).padStart(2, "0"), xs[i] + 18, 292, 54, 40, 27, color, true);
    text(s, labels[i], xs[i] + 18, 342, 132, 28, 14, C.ink, true);
    text(s, detail[i], xs[i] + 18, 382, 132, 42, 15, C.muted);
  }
  text(s, "Complete a flash, choose confidence, and continue—without a daily ceiling.", 168, 510, 944, 60, 27, C.ink, true, "center");
  text(s, "The tile remembers progress locally and returns with the next relevant lesson.", 230, 582, 820, 42, 18, C.muted, false, "center");
  note(s, "Tran, Victoria", "Walk left to right. Stress that the sequence is deterministic and category-bound: AWS remains AWS until the learner changes it.", [
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/README.md",
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/services/learning_service.py",
  ]);
}

// 5 — Learning method
{
  const s = ppt.slides.add(); chrome(s, "Learning design", 5);
  title(s, "Learning moves from clarity to application.", "The same evidence-informed sequence works across cloud, AI/ML, and digital trust.");
  addImage(s, "lesson", 90, 220, 226, 380);
  addImage(s, "scenario", 392, 220, 226, 380);
  addImage(s, "quiz", 694, 220, 226, 380);
  text(s, "CORE CONCEPT", 87, 626, 235, 26, 13, C.cyan, true, "center");
  text(s, "PRACTICAL SCENARIO", 388, 626, 242, 26, 13, C.orange, true, "center");
  text(s, "KNOWLEDGE CHECK", 694, 626, 236, 26, 13, C.mint, true, "center");
  text(s, "Go deeper is optional.\nReflection and recall make it stick.", 994, 270, 220, 110, 25, C.ink, true);
  rect(s, 996, 455, 190, 3, C.violet);
  text(s, "Clear first.\nRelevant next.\nTest differently.", 996, 492, 210, 120, 20, C.muted, false);
  note(s, "Edupuganti, Kranthima", "Use the screenshots to show that FlashTile teaches before it tests. The practical scenario is deliberately different from the quiz formulation.", [
    `${ASSET}/lesson.png`, `${ASSET}/scenario.png`, `${ASSET}/quiz.png`,
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/docs/LearningMethod.md",
  ]);
}

// 6 — Differentiation
{
  const s = ppt.slides.add(); chrome(s, "Why it stands out", 6);
  title(s, "The differentiator is delivery—not another content catalog.", "FlashTile combines a distinctive form factor with practical learning mechanics.");
  text(s, "TILE-FIRST", 86, 242, 240, 34, 15, C.cyan, true);
  text(s, "Learning stays visible at the edge of the workday.", 86, 284, 470, 72, 25, C.ink, true);
  text(s, "CATEGORY-BOUND", 690, 242, 240, 34, 15, C.orange, true);
  text(s, "The selected goal controls every following lesson.", 690, 284, 470, 72, 25, C.ink, true);
  rect(s, 86, 395, 1088, 1, C.line);
  text(s, "SMART RECALL", 86, 438, 240, 34, 15, C.violet, true);
  text(s, "Confidence schedules a different future scenario.", 86, 480, 470, 72, 25, C.ink, true);
  text(s, "HUMAN DETAILS", 690, 438, 240, 34, 15, C.mint, true);
  text(s, "Notes, bookmarks, breathing reset, and recognition support consistency.", 690, 480, 470, 82, 25, C.ink, true);
  text(s, "Small interactions. One coherent learning habit.", 86, 614, 1088, 38, 23, C.muted, false, "center");
  note(s, "Edupuganti, Kranthima", "Connect every differentiator back to learning. The breathing action and team recognition are intentionally secondary, not separate product pillars.", [
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/README.md",
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/docs/LearningMethod.md",
  ]);
}

// 7 — Current proof
{
  const s = ppt.slides.add(); chrome(s, "What works now", 7);
  title(s, "RC15 proves the complete tile-first learning loop.", "The current candidate is runnable on macOS, Windows-ready, and backed by automated checks.");
  metric(s, "15", "curated lessons", 84, 230, C.cyan);
  metric(s, "3", "learning categories", 326, 230, C.orange);
  metric(s, "29", "automated tests", 84, 420, C.mint);
  metric(s, "410×690", "fixed tile geometry", 326, 420, C.violet, 380);
  addImage(s, "progress", 842, 210, 261, 440);
  text(s, "Verified: onboarding, goal mapping, category filtering, completion, XP, notes, recall, and asset integrity.", 84, 590, 650, 58, 18, C.muted);
  note(s, "Griffin, Trey", "These are implementation facts from RC15—not adoption claims. Mention that 29 tests cover the corrected three-goal mapping and category-only navigation.", [
    `${ASSET}/progress.png`,
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/README.md",
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/tests/test_learning_service.py",
  ]);
}

// 8 — Trust
{
  const s = ppt.slides.add(); chrome(s, "Enterprise trust", 8);
  title(s, "Trust is designed in before intelligence is connected.", "The current release is local by default; future AI and identity integrations remain replaceable services.", 35, 172);
  rect(s, 80, 220, 10, 360, C.mint);
  text(s, "LOCAL TODAY", 118, 226, 300, 28, 14, C.mint, true);
  text(s, "Progress and settings stay in a local Excel workbook.", 118, 266, 450, 58, 24, C.ink, true);
  text(s, "No customer data, credentials, secrets, or confidential business information is required.", 118, 338, 470, 82, 18, C.muted);
  text(s, "CONTROLLED TOMORROW", 690, 226, 370, 28, 14, C.cyan, true);
  text(s, "SSO, grounded AI, and team services connect behind clear interfaces.", 690, 266, 470, 78, 24, C.ink, true);
  text(s, "Leaderboard participation remains optional; raw identity keys stay out of the interface; approved sources ground future content.", 690, 358, 470, 100, 18, C.muted);
  rect(s, 118, 500, 1040, 1, C.line);
  text(s, "Design principle", 118, 530, 180, 26, 15, C.orange, true);
  text(s, "Minimum data. Clear purpose. Replaceable integrations.", 320, 524, 820, 42, 27, C.ink, true);
  note(s, "Griffin, Trey", "Be explicit that RC15 does not claim production SSO or live AI. The architecture is ready for those controlled integrations after governance approval.", [
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/docs/Vision.md",
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/README.md",
  ]);
}

// 9 — Team
{
  const s = ppt.slides.add(); chrome(s, "Social learning", 9);
  title(s, "Team momentum adds encouragement without adding noise.", "Shared goals and recognition stay secondary to the individual learning experience.");
  addImage(s, "team", 92, 210, 267, 450);
  text(s, "SIX CONTRIBUTORS", 474, 210, 260, 28, 14, C.cyan, true);
  const names = [
    "Tran, Victoria", "Edupuganti, Kranthima", "Griffin, Trey",
    "Neel, Jeffrey", "Talley, Kyle", "Patel, Shrenik",
  ];
  for (let i = 0; i < names.length; i++) {
    const y = 258 + i * 52;
    text(s, String(i + 1).padStart(2, "0"), 474, y, 45, 28, 16, i === 5 ? C.orange : C.mint, true);
    text(s, names[i], 530, y - 2, 430, 32, 20, C.ink, i === 5);
  }
  rect(s, 474, 584, 650, 1, C.line);
  text(s, "Shared challenge  •  Appreciation  •  Opt-in leaderboard", 474, 610, 680, 34, 18, C.muted);
  note(s, "Neel, Jeffrey", "Position Team Board as a capability preview using local illustrative data. Emphasize privacy: no personal notes, quiz answers, or confidence ratings are shared.", [
    `${ASSET}/team.png`,
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/services/learning_service.py",
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/docs/UserTestChecklist.md",
  ]);
}

// 10 — Architecture
{
  const s = ppt.slides.add(); chrome(s, "Architecture", 10);
  title(s, "One interface connects the MVP to enterprise services.", "The UI does not need to change when storage, identity, or content providers evolve.");
  const xs = [80, 320, 560, 800, 1040];
  for (let i = 0; i < 4; i++) {
    s.shapes.add({ geometry: "rightArrow", position: { left: xs[i] + 150, top: 336, width: 70, height: 34 }, fill: C.line, line: { style: "solid", fill: "none", width: 0 } });
  }
  const nodes = [
    ["FLASH TILE", "PySide6 + QML", C.cyan],
    ["LEARNING", "Lesson + recall", C.orange],
    ["SERVICES", "Clear interfaces", C.violet],
    ["DATA", "Excel today", C.mint],
    ["ENTERPRISE", "SSO • AI • APIs", C.blue],
  ];
  for (let i = 0; i < nodes.length; i++) {
    rect(s, xs[i], 272, 170, 162, C.panel, 22, nodes[i][2]);
    text(s, nodes[i][0], xs[i] + 14, 302, 142, 28, 15, nodes[i][2], true, "center");
    text(s, nodes[i][1], xs[i] + 14, 350, 142, 54, 17, C.ink, true, "center");
  }
  text(s, "Replace the adapter—not the learning experience.", 190, 510, 900, 52, 31, C.ink, true, "center");
  text(s, "Cross-platform UI • local-first resilience • controlled upgrade path", 240, 580, 800, 34, 18, C.muted, false, "center");
  note(s, "Neel, Jeffrey", "Explain the architecture at a business level. Excel proves the workflow now; a later repository or API can replace it behind the same service boundary.", [
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/README.md",
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/services/excel_service.py",
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/services/learning_service.py",
  ]);
}

// 11 — Roadmap and measures
{
  const s = ppt.slides.add(); chrome(s, "Path to v1.0", 11);
  title(s, "The next milestone is a controlled pilot.", "Stabilize the core, measure learning behavior, then earn the right to expand.");
  rect(s, 92, 256, 1030, 5, C.line);
  const steps = [
    ["NOW", "RC15 candidate", "Mac acceptance", C.cyan],
    ["NEXT", "v1.0 release", "Windows package", C.orange],
    ["PILOT", "Small cohort", "Measure usage", C.mint],
    ["EXPAND", "Approved services", "SSO + grounded AI", C.violet],
  ];
  for (let i = 0; i < steps.length; i++) {
    const x = 88 + i * 292;
    s.shapes.add({ geometry: "ellipse", position: { left: x, top: 235, width: 48, height: 48 }, fill: steps[i][3], line: { style: "solid", fill: C.bg, width: 5 } });
    text(s, steps[i][0], x, 308, 230, 28, 14, steps[i][3], true);
    text(s, steps[i][1], x, 350, 230, 36, 23, C.ink, true);
    text(s, steps[i][2], x, 394, 230, 32, 17, C.muted);
  }
  text(s, "Measure what matters", 88, 500, 300, 38, 26, C.ink, true);
  text(s, "Activation  •  Lesson completion  •  Recall success  •  Repeat use  •  User feedback", 88, 553, 1080, 52, 20, C.muted);
  note(s, "Talley, Kyle", "The roadmap deliberately prioritizes acceptance and packaging before AI expansion. Proposed pilot measures are evaluation categories, not claimed results.", [
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/docs/Roadmap.md",
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/docs/ReleaseChecklist.md",
  ]);
}

// 12 — Close
{
  const s = ppt.slides.add();
  s.background.fill = C.bg;
  rect(s, 0, 0, 18, 720, C.cyan);
  rect(s, 18, 0, 7, 720, C.violet);
  s.images.add({ blob: IMG.logo, contentType: "image/png", alt: "FlashTile logo", fit: "contain", position: { left: 90, top: 120, width: 360, height: 420 } });
  text(s, "FlashTile brings learning\nto the employee.", 520, 140, 650, 130, 48, C.ink, true);
  text(s, "Small enough for the workday.\nPractical enough to remember.\nStructured for enterprise trust.", 524, 320, 590, 130, 25, C.muted, false);
  rect(s, 524, 500, 420, 4, C.orange);
  text(s, "OUR ASK", 524, 528, 150, 26, 14, C.orange, true);
  text(s, "Support a controlled v1.0 pilot.", 524, 566, 610, 48, 30, C.ink, true);
  text(s, "Tran, Victoria  •  Edupuganti, Kranthima  •  Griffin, Trey\nNeel, Jeffrey  •  Talley, Kyle  •  Patel, Shrenik", 86, 646, 1100, 40, 14, C.dim, false, "center");
  note(s, "Talley, Kyle", "Close by returning to the opening promise. Ask judges to evaluate FlashTile as a focused pilot candidate with a working core and a disciplined enterprise path.", [
    `${ASSET}/logo.png`,
    "/Users/shree/Documents/Codex/2026-09-03/what-is-the-latest-version/FlashTile-RC15/docs/Proposal.md",
  ]);
}

const pptx = await PresentationFile.exportPptx(ppt);
await pptx.save(OUT);
console.log(OUT);
