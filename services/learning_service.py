from __future__ import annotations

from datetime import date

from PySide6.QtCore import Property, QObject, Signal, Slot

from models.lesson import Lesson
from services.excel_service import ExcelService


LESSONS = {
    "AWS & Cloud": (
        Lesson(
            "AWS & Cloud",
            "AWS Global Infrastructure",
            "A Region is a geographic area. Each Region contains separate Availability Zones, so an application can survive a failure in one location.",
            why_it_matters="Customers expect important services to remain available even when infrastructure fails.",
            scenario="A customer-facing application runs in one Availability Zone. That facility loses power. How would using a second Availability Zone change the outcome?",
            deeper="• Regions provide geographic separation.\n• Availability Zones isolate failures inside a Region.\n• Multi-AZ designs trade added cost for resilience.",
            question="A critical application must survive one facility failure. What is the best starting design?",
            options=("One large server", "Two Availability Zones", "One storage bucket"),
            answer=1,
            explanation="Using two Availability Zones reduces dependence on a single facility.",
            recall_scenario="A web service runs across two Availability Zones, but all requests still go to one unhealthy instance.",
            recall_question="What additional capability is most important?",
            recall_options=("A health-aware load balancer", "A larger logo", "One permanent server"),
            recall_answer=0,
            recall_explanation="A health-aware load balancer can redirect requests away from unhealthy capacity.",
        ),
        Lesson(
            "AWS & Cloud",
            "The Shared Responsibility Model",
            "AWS protects the cloud infrastructure. Customers protect what they place in the cloud, including data, identities, permissions, and configurations.",
            why_it_matters="Security gaps often happen when each side assumes the other is responsible.",
            scenario="A team stores sensitive documents in Amazon S3 but accidentally allows public access. AWS kept the infrastructure operating—who owned the access configuration?",
            deeper="• AWS secures physical facilities and managed infrastructure.\n• Customers secure identities, data, and configurations.\n• Responsibility changes by service type.",
            question="Who manages customer data and access permissions in AWS?",
            options=("AWS only", "The customer", "The internet provider"),
            answer=1,
            explanation="Customers remain responsible for their data, identities, and access configuration.",
            recall_scenario="A developer accidentally publishes an access key in a public repository.",
            recall_question="Who must revoke and replace that customer credential?",
            recall_options=("AWS facilities staff", "The customer team", "The internet provider"),
            recall_answer=1,
            recall_explanation="Customer identities and credentials remain the customer’s responsibility.",
        ),
        Lesson(
            "AWS & Cloud",
            "Amazon S3 Foundations",
            "Amazon S3 stores files and other data as objects inside named containers called buckets. It is designed for high durability and broad scalability.",
            why_it_matters="Choosing the right storage service affects cost, reliability, access, and application design.",
            scenario="A team must retain millions of reports and retrieve them by name. The files do not need to behave like a server disk. Which storage pattern fits?",
            deeper="• Objects combine data with metadata and a key.\n• Buckets organize objects and enforce access policies.\n• Lifecycle rules can move older objects to cheaper storage.",
            question="What does Amazon S3 primarily store?",
            options=("Objects", "Virtual machines", "User passwords"),
            answer=0,
            explanation="Amazon S3 stores data as objects inside buckets.",
            recall_scenario="Audit reports must be kept for seven years, but older reports are rarely opened.",
            recall_question="What can reduce storage cost without deleting the reports?",
            recall_options=("An S3 lifecycle rule", "A larger EC2 instance", "More IAM users"),
            recall_answer=0,
            recall_explanation="Lifecycle rules can transition older objects to lower-cost storage classes.",
        ),
        Lesson(
            "AWS & Cloud",
            "Cloud Cost Fundamentals",
            "Cloud cost is driven by what you run, how long it runs, how much data it stores or transfers, and which service options you choose.",
            why_it_matters="Cloud resources are easy to create, so visibility and ownership are essential to prevent quiet waste.",
            scenario="A test environment runs every night and weekend even though nobody uses it. What is the simplest first cost-control action?",
            deeper="• Tag resources so teams can see ownership and purpose.\n• Budgets and alerts reveal unexpected changes.\n• Scheduling or removing idle resources cuts waste without weakening production.",
            question="Which practice gives a team early warning of unexpected cloud spending?",
            options=("Budget alerts", "Longer passwords", "More Regions"),
            answer=0,
            explanation="Budget alerts surface unusual spending before it becomes a larger surprise.",
            recall_scenario="A monthly bill grows, but finance cannot tell which team created the new resources.",
            recall_question="What would improve cost ownership most directly?",
            recall_options=("Consistent resource tags", "A larger instance", "Public access"),
            recall_answer=0,
            recall_explanation="Consistent tags connect resources and costs to an owner, environment, and purpose.",
        ),
        Lesson(
            "AWS & Cloud",
            "Serverless and Event-Driven Design",
            "Serverless services run code or workflows in response to events while the cloud provider manages the underlying servers and scaling.",
            why_it_matters="Event-driven designs can reduce operational work and align cost with actual use, but they still require monitoring and clear failure handling.",
            scenario="A small image-processing task should run only when a file arrives in storage. Which design best fits that need?",
            deeper="• Events describe that something happened.\n• Functions perform short, focused work on demand.\n• Queues and retries help absorb bursts and recover from temporary failures.",
            question="What should trigger an on-demand image-processing function?",
            options=("A file-upload event", "A permanent manual loop", "A screen saver"),
            answer=0,
            explanation="A file-upload event can invoke the function only when new work arrives.",
            recall_scenario="A burst of uploads overwhelms a downstream image service.",
            recall_question="What can buffer the work and support retries?",
            recall_options=("A queue", "A larger logo", "A public bucket"),
            recall_answer=0,
            recall_explanation="A queue decouples the producer and consumer, smoothing bursts and enabling retries.",
        ),
    ),
    "AI / ML": (
        Lesson(
            "AI / ML",
            "How Models Learn",
            "A model learns patterns from examples during training. Inference happens later, when the trained model uses those patterns to produce a prediction or response.",
            why_it_matters="Understanding training and inference helps people judge what an AI system can—and cannot—reliably do.",
            scenario="A model studies past support requests, then categorizes a new request as billing or technical. Which part is training, and which part is inference?",
            deeper="• Training adjusts a model using example data.\n• Validation checks performance on unseen examples.\n• Inference applies the trained model to new input.",
            question="What is inference?",
            options=("Training a model", "Using a model to make a prediction", "Deleting training data"),
            answer=1,
            explanation="Inference uses a trained model to produce a prediction or response.",
            recall_scenario="A trained model receives a new support request and labels it as a billing issue.",
            recall_question="Which activity is occurring now?",
            recall_options=("Inference", "Training", "Data deletion"),
            recall_answer=0,
            recall_explanation="Applying a trained model to new input is inference.",
        ),
        Lesson(
            "AI / ML",
            "Training Data Quality",
            "AI systems learn from the examples they receive. Missing, inaccurate, or unrepresentative examples can produce unreliable or unfair results.",
            why_it_matters="A sophisticated model cannot compensate for data that does not represent the problem it must solve.",
            scenario="A recommendation model was trained only on employees from one department but will be used across the organization. What should the team investigate first?",
            deeper="• Representation matters as much as data volume.\n• Historical outcomes may contain historical bias.\n• Data quality must be monitored after deployment.",
            question="What can biased training data produce?",
            options=("Guaranteed accuracy", "Biased model outputs", "Smaller file sizes"),
            answer=1,
            explanation="Models can reproduce or amplify patterns and bias present in their training data.",
            recall_scenario="A model performed well during testing but becomes less accurate after a new customer segment begins using it.",
            recall_question="What should the team investigate first?",
            recall_options=("Data drift", "Screen brightness", "File compression"),
            recall_answer=0,
            recall_explanation="A changed input population can create data drift and reduce model reliability.",
        ),
        Lesson(
            "AI / ML",
            "Human Oversight",
            "AI can support a decision, but accountable people must define boundaries, review important outcomes, and know when to override or escalate.",
            why_it_matters="Automation without ownership can turn a model error into a business, customer, or compliance failure.",
            scenario="An AI system flags an unusual transaction. Should it permanently restrict the customer automatically, or route the case for appropriate review?",
            deeper="• Risk determines the required level of oversight.\n• Escalation paths must exist before deployment.\n• Monitoring should detect drift and unexpected outcomes.",
            question="Why is human review important for consequential AI decisions?",
            options=("It removes all risk", "It adds accountable judgment", "It makes models train faster"),
            answer=1,
            explanation="Human oversight adds context, judgment, and accountability to AI-assisted decisions.",
            recall_scenario="An AI system is uncertain about a decision that could materially affect a customer.",
            recall_question="What is the safest next step?",
            recall_options=("Escalate for authorized review", "Hide the uncertainty", "Always accept the output"),
            recall_answer=0,
            recall_explanation="Consequential, uncertain outcomes should follow a defined human-review path.",
        ),
        Lesson(
            "AI / ML",
            "Evaluating AI Systems",
            "AI evaluation uses representative test cases and clear success criteria to measure quality, safety, and reliability before and after deployment.",
            why_it_matters="A compelling demo does not show how a system behaves across edge cases, changing data, or real operational conditions.",
            scenario="A support assistant sounds helpful in five demos. What should the team do before allowing broad customer use?",
            deeper="• Define measurable quality and safety criteria.\n• Test normal, difficult, and adversarial cases.\n• Monitor production behavior because performance can change over time.",
            question="What makes an AI evaluation useful?",
            options=("Representative test cases", "One favorite example", "No success criteria"),
            answer=0,
            explanation="Representative test cases show performance across the situations the system is expected to face.",
            recall_scenario="An assistant passed its original tests, but customer questions have changed over six months.",
            recall_question="What should the team do next?",
            recall_options=("Refresh and rerun evaluations", "Assume quality is unchanged", "Remove monitoring"),
            recall_answer=0,
            recall_explanation="Evaluation sets should evolve with real usage, risks, and failure patterns.",
        ),
        Lesson(
            "AI / ML",
            "Privacy in AI Workflows",
            "AI inputs can contain personal, confidential, or regulated information. Teams must minimize data and use only approved systems and retention rules.",
            why_it_matters="Once sensitive information enters an unapproved workflow, the organization may lose control over access, retention, and downstream use.",
            scenario="An employee wants to paste a customer record into a public AI tool to summarize it. What should happen first?",
            deeper="• Use the minimum data needed for the task.\n• Remove or mask sensitive fields when possible.\n• Confirm the tool, purpose, access, and retention are approved.",
            question="What is the safest starting principle for AI input data?",
            options=("Data minimization", "Copy everything", "Ignore retention"),
            answer=0,
            explanation="Data minimization reduces exposure by using only what is needed for the approved purpose.",
            recall_scenario="A team can complete an AI task using either full customer records or anonymized excerpts.",
            recall_question="Which input should it prefer?",
            recall_options=("Anonymized excerpts", "Full records", "Both by default"),
            recall_answer=0,
            recall_explanation="Anonymized excerpts reduce privacy risk while still supporting the task.",
        ),
    ),
    "Cybersecurity & Digital Trust": (
        Lesson(
            "Cybersecurity & Digital Trust",
            "The Principle of Least Privilege",
            "Give each person or system only the access required for its current task—and remove that access when it is no longer needed.",
            why_it_matters="Every unnecessary permission increases the impact of a mistake, compromised account, or malicious action.",
            scenario="A temporary analyst needs to read one report folder for two weeks. Should the analyst receive permanent administrator access or limited time-bound access?",
            deeper="• Access should be specific, temporary, and reviewable.\n• Roles are easier to govern than one-off permissions.\n• Privileged access deserves stronger verification.",
            question="What does least privilege mean?",
            options=("Give everyone admin access", "Grant only required access", "Never grant access"),
            answer=1,
            explanation="Least privilege limits access to only what a person or system needs.",
            recall_scenario="A service account finished a migration but still has administrator permissions.",
            recall_question="What should happen next?",
            recall_options=("Keep access forever", "Replace it with task-specific access", "Share the account"),
            recall_answer=1,
            recall_explanation="Permissions should be reduced when the privileged task is complete.",
        ),
        Lesson(
            "Cybersecurity & Digital Trust",
            "AI-Enabled Fraud",
            "Generative AI can imitate writing, images, and voices. A familiar-looking message is therefore not proof that the sender is genuine.",
            why_it_matters="Cyber-enabled fraud is increasingly designed to exploit trust and urgency rather than break technical controls.",
            scenario="You receive an urgent voice message that sounds like a senior leader and requests an unusual financial action. What should you do before acting?",
            deeper="• Deepfakes can imitate trusted people.\n• Urgency discourages independent verification.\n• Verify through a separate approved channel.",
            question="What is the safest response to an unusual urgent request from a familiar voice?",
            options=("Act immediately", "Verify independently", "Forward it widely"),
            answer=1,
            explanation="Independent verification breaks the attacker’s control of the communication channel.",
            recall_scenario="A convincing video call asks you to bypass an established approval step for an urgent transfer.",
            recall_question="What is the strongest response?",
            recall_options=("Use an independent approved channel", "Trust the video", "Disable all messaging"),
            recall_answer=0,
            recall_explanation="Independent verification helps detect impersonation even when media appears authentic.",
        ),
        Lesson(
            "Cybersecurity & Digital Trust",
            "Post-Quantum Readiness",
            "Future quantum computers may weaken widely used public-key cryptography. Organizations must identify affected systems and prepare a careful migration.",
            why_it_matters="Sensitive information captured today may still require protection years from now.",
            scenario="A system stores information that must remain confidential for decades. Why should its team inventory cryptographic dependencies now?",
            deeper="• Migration can take years across complex estates.\n• Crypto-agility makes algorithms replaceable.\n• NIST has standardized initial post-quantum algorithms.",
            question="What is a practical first step toward post-quantum readiness?",
            options=("Inventory cryptography", "Delete all encryption", "Wait for a breach"),
            answer=0,
            explanation="An inventory identifies where vulnerable algorithms exist and what must be migrated.",
            recall_scenario="A large application depends on cryptography embedded across many vendors and services.",
            recall_question="Which capability will make future algorithm replacement easier?",
            recall_options=("Crypto-agility", "Permanent hard-coding", "Removing all encryption"),
            recall_answer=0,
            recall_explanation="Crypto-agility allows algorithms and keys to be replaced without redesigning the entire system.",
        ),
        Lesson(
            "Cybersecurity & Digital Trust",
            "Zero Trust Foundations",
            "Zero trust means no user, device, or request is trusted automatically. Access is verified explicitly and limited to what is needed.",
            why_it_matters="A network location alone cannot prove that a request is safe, especially with remote work, cloud systems, and stolen credentials.",
            scenario="An employee signs in from a new unmanaged device to access sensitive data. What should the system evaluate before granting access?",
            deeper="• Verify identity with strong authentication.\n• Consider device health, context, and resource sensitivity.\n• Recheck trust as risk changes instead of granting permanent broad access.",
            question="Which statement best describes zero trust?",
            options=("Verify explicitly", "Trust every internal device", "Disable all access"),
            answer=0,
            explanation="Zero trust continuously verifies access using identity, device, context, and policy.",
            recall_scenario="A valid account begins making unusual requests from an unfamiliar location.",
            recall_question="What should a zero-trust system do?",
            recall_options=("Re-evaluate the request", "Trust it forever", "Share the session"),
            recall_answer=0,
            recall_explanation="Changed context should trigger a fresh risk and access decision.",
        ),
        Lesson(
            "Cybersecurity & Digital Trust",
            "Incident Response Basics",
            "Incident response is a prepared process for detecting, containing, investigating, recovering from, and learning after a security event.",
            why_it_matters="Clear roles and practiced steps reduce confusion when time, evidence, and customer trust are at risk.",
            scenario="A workstation shows signs of compromise. Should an employee investigate alone or follow the approved reporting and containment process?",
            deeper="• Report quickly through the approved channel.\n• Preserve evidence and avoid uncoordinated changes.\n• Contain the threat, recover safely, and improve controls afterward.",
            question="What is the best first action when you suspect a security incident?",
            options=("Use the approved reporting process", "Delete all evidence", "Post it publicly"),
            answer=0,
            explanation="Fast reporting activates trained responders and preserves a coordinated response.",
            recall_scenario="A responder discovers a compromised device that is still connected and spreading malicious traffic.",
            recall_question="What is the immediate priority?",
            recall_options=("Contain the affected device", "Rename it", "Ignore the traffic"),
            recall_answer=0,
            recall_explanation="Containment limits further harm while the team preserves evidence and investigates.",
        ),
    ),
}

# Prepared demo paths for the free-form learning-goal experience. These remain
# local and deterministic until an approved AI content service is connected.
LESSONS.update(
    {
        "Risk & Governance": (
            Lesson(
                "Risk & Governance",
                "Risk-Informed Decision Making",
                "Risk-informed decisions compare likely outcomes, impact, uncertainty, and trade-offs before choosing a course of action.",
                why_it_matters="A structured view of risk improves judgment without pretending uncertainty can be eliminated.",
                scenario="A team can ship a reporting change quickly with limited testing or delay it for stronger validation. How should the decision be framed?",
                deeper="• Identify affected stakeholders and obligations.\n• Compare likelihood, impact, and reversibility.\n• Record the decision, owner, and monitoring plan.",
                question="What is the best basis for a risk-informed decision?",
                options=("Evidence, impact, and trade-offs", "Speed alone", "The loudest opinion"),
                answer=0,
                explanation="Good decisions make evidence, uncertainty, impact, and trade-offs visible.",
                recall_scenario="Two options offer similar value, but one creates a difficult-to-reverse control gap.",
                recall_question="What deserves special weight?",
                recall_options=("Reversibility and control impact", "Logo color", "Meeting length"),
                recall_answer=0,
                recall_explanation="Hard-to-reverse control impacts deserve explicit consideration.",
            ),
            Lesson(
                "Risk & Governance",
                "BCBS 239 & Data Governance",
                "Effective data governance defines ownership, quality, lineage, controls, and accountability so risk information can be trusted.",
                why_it_matters="Reliable decisions and reporting depend on knowing where critical data came from and whether it is complete and accurate.",
                scenario="A risk report contains a material number that cannot be traced to its source. What capability is missing?",
                deeper="• Ownership makes accountability clear.\n• Lineage traces data from source to report.\n• Quality controls test completeness, accuracy, and timeliness.",
                question="Which capability traces a reported value back to its source?",
                options=("Data lineage", "Screen sharing", "File naming"),
                answer=0,
                explanation="Data lineage documents how data moves and changes from source to use.",
                recall_scenario="Two teams publish different totals for the same risk measure.",
                recall_question="What should happen first?",
                recall_options=("Reconcile definitions, sources, and controls", "Choose the larger total", "Publish both silently"),
                recall_answer=0,
                recall_explanation="Shared definitions and traceable sources are necessary to resolve inconsistent reporting.",
            ),
            Lesson(
                "Risk & Governance",
                "Human-in-the-Loop AI Controls",
                "Human-in-the-loop control means accountable people define AI boundaries, review consequential outcomes, and can intervene or escalate.",
                why_it_matters="AI can accelerate work, but it does not transfer accountability away from the organization.",
                scenario="An AI system proposes a material reporting adjustment. What must happen before the adjustment is accepted?",
                deeper="• Match oversight to impact and uncertainty.\n• Preserve evidence of inputs, outputs, and approval.\n• Define fallback and escalation paths before use.",
                question="Who remains accountable for a consequential AI-assisted decision?",
                options=("The approved human decision owner", "The model", "No one"),
                answer=0,
                explanation="The authorized human and organization remain accountable for the decision.",
                recall_scenario="The model confidence is low and the outcome could affect regulatory reporting.",
                recall_question="What is the safest next step?",
                recall_options=("Route to qualified review", "Accept automatically", "Hide the uncertainty"),
                recall_answer=0,
                recall_explanation="High-impact uncertainty should trigger qualified human review.",
            ),
            Lesson(
                "Risk & Governance",
                "Issues & Errors Management",
                "Issues and errors management identifies problems, contains impact, finds root causes, assigns owners, and verifies sustainable remediation.",
                why_it_matters="Closing an issue without proving the fix works allows the same failure to return.",
                scenario="A recurring reporting error is corrected each month but keeps returning. What is missing?",
                deeper="• Contain immediate impact.\n• Diagnose root cause, not only symptoms.\n• Validate remediation with evidence before closure.",
                question="When should an issue be considered sustainably closed?",
                options=("After the fix is validated", "When the ticket is old", "After a verbal promise"),
                answer=0,
                explanation="Closure requires evidence that remediation addresses the root cause and operates effectively.",
                recall_scenario="A control is redesigned after an error, but nobody tests the new process.",
                recall_question="What remains incomplete?",
                recall_options=("Remediation validation", "Issue naming", "Calendar scheduling"),
                recall_answer=0,
                recall_explanation="The organization needs evidence that the redesigned control works.",
            ),
            Lesson(
                "Risk & Governance",
                "Legal-Obligation Impact Assessment",
                "An impact assessment translates a legal or regulatory change into affected processes, data, controls, technology, owners, and deadlines.",
                why_it_matters="A requirement is not operationalized until its real business and control impacts are understood and owned.",
                scenario="A new obligation changes data-retention requirements. Which areas should be assessed?",
                deeper="• Confirm scope and interpretation with qualified experts.\n• Map impacted processes, systems, data, and controls.\n• Assign accountable actions and retain evidence.",
                question="What is the output of a useful impact assessment?",
                options=("Owned actions tied to affected areas", "A copied regulation", "An informal chat"),
                answer=0,
                explanation="A useful assessment turns the obligation into traceable, owned implementation actions.",
                recall_scenario="A legal change is documented, but no system or control owner is assigned.",
                recall_question="What is the main gap?",
                recall_options=("Accountable implementation ownership", "Font size", "Meeting location"),
                recall_answer=0,
                recall_explanation="Without ownership, the required change may not be implemented or evidenced.",
            ),
        ),
        "Investment Fundamentals": (
            Lesson(
                "Investment Fundamentals",
                "Understanding Alternative Investments",
                "Alternative investments are assets or strategies outside traditional public stocks, bonds, and cash, such as private equity, private credit, real assets, and hedge funds.",
                why_it_matters="The label covers very different structures, risks, costs, and liquidity terms.",
                scenario="An investor sees two funds both labeled alternative. One owns infrastructure; the other uses a trading strategy. Should they be evaluated as interchangeable?",
                deeper="• Understand the underlying exposure and strategy.\n• Review liquidity, valuation, fees, and leverage.\n• Consider suitability within the whole portfolio.",
                question="What should be understood first about an alternative investment?",
                options=("Its underlying strategy and risks", "Its marketing name", "Its logo"),
                answer=0,
                explanation="The underlying exposure and structure determine how the investment may behave.",
                recall_scenario="A product has attractive historical returns but complex redemption limits.",
                recall_question="What should receive close review?",
                recall_options=("Liquidity terms", "Website color", "Ticker length"),
                recall_answer=0,
                recall_explanation="Liquidity limits can materially affect whether and when capital can be accessed.",
            ),
            Lesson(
                "Investment Fundamentals",
                "Diversification Beyond Labels",
                "Diversification depends on how investments behave together, not simply on owning more product names.",
                why_it_matters="Assets that appear different may become highly correlated during market stress.",
                scenario="A portfolio adds three funds that all depend on the same economic factor. Has it necessarily diversified?",
                deeper="• Examine drivers of return and loss.\n• Test correlations in normal and stressed markets.\n• Avoid concentration hidden behind different labels.",
                question="What makes an asset a useful diversifier?",
                options=("Different risk and return drivers", "A different fund name", "A higher fee"),
                answer=0,
                explanation="Diversification comes from distinct underlying drivers, especially when conditions change.",
                recall_scenario="Two strategies look uncorrelated in calm markets but fall together during stress.",
                recall_question="Which analysis was most important?",
                recall_options=("Stress correlation", "Logo comparison", "Alphabetical sorting"),
                recall_answer=0,
                recall_explanation="Stress behavior reveals diversification limits that normal-period averages can hide.",
            ),
            Lesson(
                "Investment Fundamentals",
                "Liquidity, Valuation & Fees",
                "Some alternatives trade infrequently, use model-based valuations, restrict withdrawals, and layer management or performance fees.",
                why_it_matters="Reported returns may not reveal how quickly value can change or capital can be accessed.",
                scenario="An investor may need funds next year, but a product locks capital for five years. What is the central mismatch?",
                deeper="• Match lockups to expected cash needs.\n• Understand valuation frequency and methodology.\n• Evaluate all fees and their effect on net returns.",
                question="Why must liquidity terms be reviewed before investing?",
                options=("Capital may not be available when needed", "They change the font", "They guarantee returns"),
                answer=0,
                explanation="Lockups and redemption limits can prevent timely access to invested capital.",
                recall_scenario="A fund reports stable values because holdings are priced quarterly rather than daily.",
                recall_question="What should the investor recognize?",
                recall_options=("Apparent stability may reflect valuation timing", "Risk disappeared", "Fees are zero"),
                recall_answer=0,
                recall_explanation="Infrequent valuation can smooth reported changes without eliminating economic risk.",
            ),
            Lesson(
                "Investment Fundamentals",
                "Income, Inflation & Capital Preservation",
                "Some real assets, private credit, or contractual cash flows may support income or inflation sensitivity, but none provides universal protection.",
                why_it_matters="A portfolio role should be evaluated using evidence and scenarios, not assumed from a product label.",
                scenario="A real-asset strategy is described as an inflation hedge. What should be tested before relying on that claim?",
                deeper="• Identify the mechanism linking returns to inflation.\n• Compare results across different inflation regimes.\n• Consider leverage, costs, and downside risk.",
                question="What is the right way to assess an inflation-protection claim?",
                options=("Test the mechanism and evidence", "Assume the label is enough", "Ignore downside risk"),
                answer=0,
                explanation="The expected protection should be supported by a clear mechanism and evidence across scenarios.",
                recall_scenario="An income strategy offers a high yield by taking significant credit risk.",
                recall_question="What should be evaluated with the income?",
                recall_options=("Risk of loss and default", "Only the headline yield", "Brand popularity"),
                recall_answer=0,
                recall_explanation="Yield must be considered together with the risks taken to generate it.",
            ),
            Lesson(
                "Investment Fundamentals",
                "Due Diligence & Portfolio Fit",
                "Due diligence evaluates the manager, strategy, operations, conflicts, performance evidence, legal terms, and fit with an investor's objectives and constraints.",
                why_it_matters="An attractive strategy can still be unsuitable because of concentration, liquidity, governance, or operational risk.",
                scenario="A fund has strong returns but unclear valuation controls and key-person dependence. What should happen next?",
                deeper="• Review people, process, controls, and service providers.\n• Challenge performance and risk assumptions.\n• Assess fit, sizing, and monitoring before commitment.",
                question="What is the purpose of investment due diligence?",
                options=("Understand risks, controls, and suitability", "Guarantee performance", "Replace all professional advice"),
                answer=0,
                explanation="Due diligence supports an informed suitability decision; it cannot guarantee an outcome.",
                recall_scenario="A strategy is credible but would create excessive concentration in one risk factor.",
                recall_question="What is the appropriate conclusion?",
                recall_options=("Good product, poor portfolio fit", "Automatically invest", "Ignore concentration"),
                recall_answer=0,
                recall_explanation="Portfolio fit matters independently from the quality of the product itself.",
            ),
        ),
    }
)

PRIMARY_TOPICS = ("AWS & Cloud", "AI / ML", "Cybersecurity & Digital Trust")

TOPIC_ALIASES = {
    "AWS Cloud": "AWS & Cloud",
    "Artificial Intelligence": "AI / ML",
    "Cybersecurity": "Cybersecurity & Digital Trust",
}

LEARNING_GOALS = {
    "Build resilient cloud skills": tuple(
        ("AWS & Cloud", lesson.title) for lesson in LESSONS["AWS & Cloud"]
    ),
    "Use AI responsibly": tuple(
        ("AI / ML", lesson.title) for lesson in LESSONS["AI / ML"]
    ),
    "Strengthen digital trust": tuple(
        ("Cybersecurity & Digital Trust", lesson.title)
        for lesson in LESSONS["Cybersecurity & Digital Trust"]
    ),
    "Navigate risk and governance decisions": tuple(
        ("Risk & Governance", lesson.title) for lesson in LESSONS["Risk & Governance"]
    ),
    "Understand alternative investments": tuple(
        ("Investment Fundamentals", lesson.title)
        for lesson in LESSONS["Investment Fundamentals"]
    ),
}

TOPIC_LEARNING_GOALS = {
    "AWS & Cloud": "Build resilient cloud skills",
    "AI / ML": "Use AI responsibly",
    "Cybersecurity & Digital Trust": "Strengthen digital trust",
    "Risk & Governance": "Navigate risk and governance decisions",
    "Investment Fundamentals": "Understand alternative investments",
}

LEARNING_GOAL_SUMMARIES = {
    "Balanced digital foundations": "A six-flash path across cloud, responsible AI, and digital trust.",
    "Build resilient cloud skills": "Cloud architecture, security, storage, cost, and event-driven design.",
    "Use AI responsibly": "AI fundamentals, data quality, oversight, evaluation, and privacy.",
    "Strengthen digital trust": "Access, fraud defense, cryptography, zero trust, and incident response.",
    "Navigate risk and governance decisions": "Risk decisions, BCBS 239, AI controls, issue remediation, and legal-impact assessment.",
    "Understand alternative investments": "Portfolio role, diversification, liquidity, valuation, fees, and due diligence.",
}

PREPARED_LEARNING_TOPICS = {
    "Risk & Decision Making": (
        "Navigate risk and governance decisions",
        "Risk & Governance",
        "Risk-Informed Decision Making",
    ),
    "BCBS 239 & Data Governance": (
        "Navigate risk and governance decisions",
        "Risk & Governance",
        "BCBS 239 & Data Governance",
    ),
    "Human-in-the-loop AI controls": (
        "Navigate risk and governance decisions",
        "Risk & Governance",
        "Human-in-the-Loop AI Controls",
    ),
    "Issues & Errors Management": (
        "Navigate risk and governance decisions",
        "Risk & Governance",
        "Issues & Errors Management",
    ),
    "Legal-obligation impact assessments": (
        "Navigate risk and governance decisions",
        "Risk & Governance",
        "Legal-Obligation Impact Assessment",
    ),
    "Alternative investments and portfolio diversification": (
        "Understand alternative investments",
        "Investment Fundamentals",
        "Understanding Alternative Investments",
    ),
}

DISCOVERY_ITEMS = (
    {
        "category": "General Knowledge",
        "title": "Why the sky looks blue",
        "body": "Air molecules scatter shorter blue wavelengths of sunlight more strongly than longer red wavelengths, so blue light reaches our eyes from across the sky.",
        "context": "At sunrise and sunset, sunlight travels through more atmosphere, leaving more reds and oranges in the direct light.",
        "source": "NASA Space Place",
        "source_url": "https://spaceplace.nasa.gov/blue-sky/en/",
    },
    {
        "category": "History Spotlight",
        "title": "The Rosetta Stone",
        "body": "The Rosetta Stone carries one decree in three scripts. Comparing them helped scholars decipher Egyptian hieroglyphs in the nineteenth century.",
        "context": "The breakthrough shows how a shared message can unlock an unfamiliar writing system.",
        "source": "The British Museum",
        "source_url": "https://www.britishmuseum.org/blog/everything-you-ever-wanted-know-about-rosetta-stone",
    },
    {
        "category": "Important Milestone",
        "title": "Smallpox eradication",
        "body": "In 1980, the World Health Assembly declared smallpox eradicated after a coordinated global vaccination and surveillance campaign.",
        "context": "It remains the only human infectious disease eradicated worldwide.",
        "source": "World Health Organization",
        "source_url": "https://www.who.int/emergencies/situations/smallpox",
    },
    {
        "category": "General Knowledge",
        "title": "A day is not exactly 24 hours",
        "body": "Earth completes one rotation relative to distant stars in about 23 hours and 56 minutes. Our 24-hour solar day also accounts for Earth moving around the Sun.",
        "context": "That four-minute difference is why stars rise slightly earlier each night.",
        "source": "NASA Earth Science",
        "source_url": "https://science.nasa.gov/earth/facts/",
    },
    {
        "category": "History Spotlight",
        "title": "The printing press",
        "body": "Movable-type printing existed earlier in Asia. In fifteenth-century Europe, Gutenberg's press helped make books faster and less expensive to reproduce at scale.",
        "context": "Cheaper copying accelerated the spread of literacy, scientific ideas, and public debate.",
        "source": "Library of Congress",
        "source_url": "https://www.loc.gov/item/03008887/",
    },
    {
        "category": "Important Milestone",
        "title": "The Universal Declaration of Human Rights",
        "body": "The United Nations General Assembly adopted the Universal Declaration of Human Rights in 1948 as a common standard of rights and freedoms.",
        "context": "Its thirty articles influenced constitutions, treaties, and human-rights law around the world.",
        "source": "United Nations",
        "source_url": "https://www.un.org/en/about-us/universal-declaration-of-human-rights/",
    },
    {
        "category": "General Knowledge",
        "title": "Why ice floats",
        "body": "Water expands as it freezes into an open crystal structure. Solid ice is therefore less dense than liquid water and floats.",
        "context": "Floating ice insulates the water below, helping aquatic ecosystems survive cold seasons.",
        "source": "U.S. Geological Survey",
        "source_url": "https://www.usgs.gov/water-science-school/science/water-density",
    },
    {
        "category": "History Spotlight",
        "title": "Apollo 11",
        "body": "Apollo 11 carried Neil Armstrong, Buzz Aldrin, and Michael Collins to the Moon in 1969. Armstrong and Aldrin became the first people to walk there.",
        "context": "The mission depended on years of engineering, testing, navigation, and teamwork across thousands of roles.",
        "source": "NASA",
        "source_url": "https://www.nasa.gov/missions/apollo/apollo-11/apollo-11-mission-overview/",
    },
    {
        "category": "Important Milestone",
        "title": "The internet adopts TCP/IP",
        "body": "On January 1, 1983, ARPANET transitioned to the TCP/IP protocol suite, allowing different networks to communicate through a common standard.",
        "context": "That shared protocol foundation became a defining step toward today's internet.",
        "source": "DARPA",
        "source_url": "https://www.darpa.mil/news/features/arpanet",
    },
    {
        "category": "General Knowledge",
        "title": "The atmosphere is mostly nitrogen",
        "body": "Dry air near Earth's surface is roughly 78 percent nitrogen and 21 percent oxygen, with argon, carbon dioxide, and other gases making up the rest.",
        "context": "Small concentrations of gases such as carbon dioxide can still have major effects on climate and life.",
        "source": "NASA Earth Science",
        "source_url": "https://science.nasa.gov/earth/facts/",
    },
    {
        "category": "History Spotlight",
        "title": "The Magna Carta",
        "body": "King John sealed Magna Carta in 1215 after conflict with English barons. Although many clauses addressed medieval disputes, it became a lasting symbol that rulers are subject to law.",
        "context": "Later generations connected that principle to due process and limits on government power.",
        "source": "UK Parliament",
        "source_url": "https://commonslibrary.parliament.uk/magna-carta-does-it-still-matter/",
    },
    {
        "category": "Important Milestone",
        "title": "The first powered flight",
        "body": "In 1903, the Wright brothers completed controlled, sustained flights in a powered aircraft near Kitty Hawk, North Carolina.",
        "context": "Their success combined aerodynamic research, control systems, propulsion, and repeated experimentation.",
        "source": "U.S. National Park Service",
        "source_url": "https://www.nps.gov/wrbr/learn/historyculture/thefirstflight.htm",
    },
)

TEAM_BOARD_DEMO = {
    "name": "Cloud Pioneers",
    "weekly_completed": 26,
    "weekly_goal": 35,
    "xp": 1850,
    "streak": 6,
    "challenge": "Complete 35 lessons together",
    "challenge_reward": "Unlock the Knowledge Crew badge",
    "members": (
        ("Tran, Victoria", "AI / ML", "5 lessons", "340 XP"),
        ("Edupuganti, Kranthima", "AWS & Cloud", "5 lessons", "325 XP"),
        ("Griffin, Trey", "Digital Trust", "4 lessons", "310 XP"),
        ("Neel, Jeffrey", "AWS & Cloud", "4 lessons", "295 XP"),
        ("Talley, Kyle", "AI / ML", "4 lessons", "285 XP"),
        ("Patel, Shrenik (You)", "Balanced Path", "4 lessons", "295 XP"),
    ),
}

BADGES = (
    ("✦", "First Step", "Complete your first lesson", "completed", 1),
    ("↗", "Momentum", "Build a 3-day learning streak", "streak", 3),
    ("✎", "Knowledge Keeper", "Save 3 quick notes", "notes", 3),
    ("◆", "Curator", "Save 3 lessons", "bookmarks", 3),
    ("✓", "Mastery Maker", "Master one lesson", "mastered", 1),
    ("◎", "Explorer", "Learn across all 3 topics", "completed_topics", 3),
)

DEMO_TOUR = (
    ("Welcome to FlashTile", "A focused learning tile that turns short lessons into recall, reflection, and measurable progress."),
    ("Set a Learning Goal", "Choose a curated path from the first footer button. FlashTile sequences lessons across the skills you want to build."),
    ("Learn, Apply, Recall", "Each flash moves from a core concept to a practical scenario, deeper context, and a knowledge check."),
    ("Keep What Matters", "Save lessons and capture quick takeaways. Everything stays in the local workbook on this computer."),
    ("Reset Your Focus", "The Meditation button provides a guided 60-second breathing break, with reduced-motion support."),
    ("Discover Something Daily", "Daily Discovery rotates through general knowledge and history, with a visible authoritative source."),
    ("Show Team Capability", "Team Board demonstrates shared goals and a weekly challenge. Personal Progress shows badges and measurable growth."),
)


class LearningService(QObject):
    changed = Signal()
    celebration = Signal(str)
    quizResult = Signal(str, bool)

    def __init__(self) -> None:
        super().__init__()
        self.store = ExcelService()
        stored_topic = self.store.selected_topic()
        self._topic = TOPIC_ALIASES.get(stored_topic, stored_topic)
        if self._topic not in LESSONS:
            self._topic = "AWS & Cloud"
        self._lesson_index = self.store.lesson_index(self._topic) % len(LESSONS[self._topic])
        self._learning_goal = self.store.learning_goal()
        if self._learning_goal == "Balanced digital foundations":
            self._learning_goal = TOPIC_LEARNING_GOALS[self._topic]
            self.store.set_learning_goal(self._learning_goal)
            self.store.set_learning_goal_position(0)
        if self._learning_goal not in LEARNING_GOALS:
            self._learning_goal = ""
        self._goal_position = 0
        if self._learning_goal:
            sequence = LEARNING_GOALS[self._learning_goal]
            self._goal_position = self.store.learning_goal_position() % len(sequence)
            goal_topic, goal_title = sequence[self._goal_position]
            goal_index = self._find_lesson(goal_topic, goal_title)
            if goal_index is not None:
                self._topic = goal_topic
                self._lesson_index = goal_index
        self._reduced_motion = self.store.reduced_motion()
        self._welcome_seen = self.store.welcome_seen()
        self._discovery_offset = 0
        self._search_query = ""
        self._tour_step = 0
        self._resume_topic = self._topic
        self._resume_lesson_index = self._lesson_index
        self._xp, self._streak = self.store.totals()
        self._quiz_passed = False
        self._review_mode = False
        self._activate_due_review()
        self._load_lesson_tools()

    def _lesson(self) -> Lesson:
        return LESSONS[self._topic][self._lesson_index]

    def _discovery(self) -> dict[str, str]:
        index = (date.today().toordinal() + self._discovery_offset) % len(
            DISCOVERY_ITEMS
        )
        return DISCOVERY_ITEMS[index]

    def _find_lesson(self, topic: str, title: str) -> int | None:
        for index, lesson in enumerate(LESSONS.get(topic, ())):
            if lesson.title == title:
                return index
        return None

    def _open_lesson(self, topic: str, title: str, *, clear_goal: bool = False) -> bool:
        lesson_index = self._find_lesson(topic, title)
        if lesson_index is None:
            return False
        self._topic = topic
        self._lesson_index = lesson_index
        self._resume_topic = topic
        self._resume_lesson_index = lesson_index
        self._review_mode = False
        self._quiz_passed = False
        if clear_goal:
            self._learning_goal = ""
            self._goal_position = 0
            self.store.set_learning_goal("")
            self.store.set_learning_goal_position(0)
        self.store.set_selected_topic(topic)
        self.store.set_lesson_index(topic, lesson_index)
        self._load_lesson_tools()
        self.changed.emit()
        return True

    def _activate_due_review(self) -> bool:
        for topic, title in self.store.due_reviews():
            index = self._find_lesson(topic, title)
            if index is not None:
                self._topic = topic
                self._lesson_index = index
                self._review_mode = True
                return True
        return False

    def _load_lesson_tools(self) -> None:
        lesson = self._lesson()
        self._bookmarked = self.store.is_bookmarked(lesson.topic, lesson.title)
        self._lesson_note = self.store.lesson_note(lesson.topic, lesson.title)
        self._review_state = self.store.review_state(lesson.topic, lesson.title)

    def _progress(self) -> dict[str, object]:
        return self.store.progress_summary(
            sum(len(LESSONS[topic]) for topic in PRIMARY_TOPICS),
            set(PRIMARY_TOPICS),
        )

    def _search_results(self) -> list[tuple[str, str]]:
        query = self._search_query.strip().casefold()
        results = []
        for lesson in LESSONS[self._topic]:
            searchable = f"{self._topic} {lesson.title} {lesson.description}".casefold()
            if not query or query in searchable:
                results.append((self._topic, lesson.title))
        return results

    @staticmethod
    def _mastery_label(level: int) -> str:
        return ("New", "Learning", "Practicing", "Mastered")[max(0, min(3, level))]

    @Property("QStringList", constant=True)
    def topics(self) -> list[str]:
        return list(LESSONS)

    @Property(str, notify=changed)
    def topic(self) -> str:
        return self._topic

    @Property(str, notify=changed)
    def title(self) -> str:
        return self._lesson().title

    @Property(str, notify=changed)
    def description(self) -> str:
        return self._lesson().description

    @Property(str, notify=changed)
    def whyItMatters(self) -> str:
        return self._lesson().why_it_matters

    @Property(str, notify=changed)
    def scenario(self) -> str:
        lesson = self._lesson()
        return lesson.recall_scenario if self._review_mode else lesson.scenario

    @Property(str, notify=changed)
    def deeper(self) -> str:
        return self._lesson().deeper

    @Property(int, notify=changed)
    def minutes(self) -> int:
        return self._lesson().minutes

    @Property(int, notify=changed)
    def xp(self) -> int:
        return self._xp

    @Property(int, notify=changed)
    def streak(self) -> int:
        return self._streak

    @Property(str, notify=changed)
    def question(self) -> str:
        lesson = self._lesson()
        return lesson.recall_question if self._review_mode else lesson.question

    @Property("QStringList", notify=changed)
    def options(self) -> list[str]:
        lesson = self._lesson()
        return list(lesson.recall_options if self._review_mode else lesson.options)

    @Property(bool, notify=changed)
    def quizPassed(self) -> bool:
        return self._quiz_passed

    @Property(bool, notify=changed)
    def bookmarked(self) -> bool:
        return self._bookmarked

    @Property(str, notify=changed)
    def lessonNote(self) -> str:
        return self._lesson_note

    @Property(int, notify=changed)
    def noteCount(self) -> int:
        return len(self.store.notes())

    @Property("QStringList", notify=changed)
    def noteItems(self) -> list[str]:
        return [
            f"{title}  •  {note[:72]}{'…' if len(note) > 72 else ''}"
            for _, title, note in self.store.notes()
        ]

    @Property("QStringList", constant=True)
    def learningGoals(self) -> list[str]:
        return [TOPIC_LEARNING_GOALS[topic] for topic in PRIMARY_TOPICS]

    @Property("QStringList", constant=True)
    def preparedLearningTopics(self) -> list[str]:
        return list(PREPARED_LEARNING_TOPICS)

    @Property("QStringList", constant=True)
    def topLearningItems(self) -> list[str]:
        return [*PRIMARY_TOPICS, *PREPARED_LEARNING_TOPICS]

    @Property(str, notify=changed)
    def currentTopLearningItem(self) -> str:
        for label, (_, topic, title) in PREPARED_LEARNING_TOPICS.items():
            if self._topic == topic and (
                self._lesson().title == title or topic == "Investment Fundamentals"
            ):
                return label
        return self._topic

    @Property(str, notify=changed)
    def defaultLearningGoal(self) -> str:
        return TOPIC_LEARNING_GOALS[self._topic]

    @Property(str, notify=changed)
    def learningGoal(self) -> str:
        return self._learning_goal

    @Property(bool, notify=changed)
    def goalActive(self) -> bool:
        return bool(self._learning_goal)

    @Property(str, notify=changed)
    def learningGoalSummary(self) -> str:
        if not self._learning_goal:
            return "Choose a curated path that matches what you want to learn."
        return LEARNING_GOAL_SUMMARIES[self._learning_goal]

    @Slot(str, result=str)
    def describeLearningGoal(self, goal: str) -> str:
        return LEARNING_GOAL_SUMMARIES.get(goal, "")

    @Property(str, notify=changed)
    def goalProgressText(self) -> str:
        if not self._learning_goal:
            return "No guided path selected"
        total = len(LEARNING_GOALS[self._learning_goal])
        return f"Flash {self._goal_position + 1} of {total}"

    @Property(bool, notify=changed)
    def reducedMotion(self) -> bool:
        return self._reduced_motion

    @Property(bool, notify=changed)
    def welcomeSeen(self) -> bool:
        return self._welcome_seen

    @Property(str, notify=changed)
    def dailyDiscoveryDate(self) -> str:
        today = date.today()
        return f"{today.strftime('%B')} {today.day}"

    @Property(str, notify=changed)
    def dailyDiscoveryCategory(self) -> str:
        return self._discovery()["category"]

    @Property(str, notify=changed)
    def dailyDiscoveryTitle(self) -> str:
        return self._discovery()["title"]

    @Property(str, notify=changed)
    def dailyDiscoveryBody(self) -> str:
        return self._discovery()["body"]

    @Property(str, notify=changed)
    def dailyDiscoveryContext(self) -> str:
        return self._discovery()["context"]

    @Property(str, notify=changed)
    def dailyDiscoverySource(self) -> str:
        return self._discovery()["source"]

    @Property(str, notify=changed)
    def dailyDiscoverySourceUrl(self) -> str:
        return self._discovery()["source_url"]

    @Property(str, constant=True)
    def teamName(self) -> str:
        return str(TEAM_BOARD_DEMO["name"])

    @Property(int, constant=True)
    def teamWeeklyCompleted(self) -> int:
        return int(TEAM_BOARD_DEMO["weekly_completed"])

    @Property(int, constant=True)
    def teamWeeklyGoal(self) -> int:
        return int(TEAM_BOARD_DEMO["weekly_goal"])

    @Property(int, constant=True)
    def teamXp(self) -> int:
        return int(TEAM_BOARD_DEMO["xp"])

    @Property(int, constant=True)
    def teamStreak(self) -> int:
        return int(TEAM_BOARD_DEMO["streak"])

    @Property(str, constant=True)
    def teamChallenge(self) -> str:
        return str(TEAM_BOARD_DEMO["challenge"])

    @Property(str, constant=True)
    def teamChallengeReward(self) -> str:
        return str(TEAM_BOARD_DEMO["challenge_reward"])

    @Property("QStringList", constant=True)
    def teamMemberItems(self) -> list[str]:
        return ["|".join(member) for member in TEAM_BOARD_DEMO["members"]]

    @Property(int, notify=changed)
    def progressCompleted(self) -> int:
        return int(self._progress()["completed"])

    @Property(int, constant=True)
    def progressTotal(self) -> int:
        return sum(len(LESSONS[topic]) for topic in PRIMARY_TOPICS)

    @Property(int, notify=changed)
    def progressPercent(self) -> int:
        return int(self._progress()["percent"])

    @Property(int, notify=changed)
    def progressMastered(self) -> int:
        return int(self._progress()["mastered"])

    @Property(int, notify=changed)
    def progressDueReviews(self) -> int:
        return int(self._progress()["due_reviews"])

    @Property("QStringList", notify=changed)
    def progressTopicItems(self) -> list[str]:
        counts = self._progress()["topic_counts"]
        return [
            f"{topic}|{int(counts.get(topic, 0))}|{len(LESSONS[topic])}"
            for topic in PRIMARY_TOPICS
        ]

    @Property("QStringList", notify=changed)
    def badgeItems(self) -> list[str]:
        progress = self._progress()
        values = {**progress, "streak": self._streak}
        return [
            f"{icon}|{name}|{description}|{1 if int(values[key]) >= target else 0}"
            for icon, name, description, key, target in BADGES
        ]

    @Property(int, notify=changed)
    def unlockedBadgeCount(self) -> int:
        return sum(item.endswith("|1") for item in self.badgeItems)

    @Property("QStringList", notify=changed)
    def searchLessonItems(self) -> list[str]:
        return [f"{topic}|{title}" for topic, title in self._search_results()]

    @Property(int, notify=changed)
    def searchResultCount(self) -> int:
        return len(self._search_results())

    @Property(str, notify=changed)
    def tourTitle(self) -> str:
        return DEMO_TOUR[self._tour_step][0]

    @Property(str, notify=changed)
    def tourBody(self) -> str:
        return DEMO_TOUR[self._tour_step][1]

    @Property(str, notify=changed)
    def tourProgressText(self) -> str:
        return f"{self._tour_step + 1} of {len(DEMO_TOUR)}"

    @Property(int, notify=changed)
    def tourStep(self) -> int:
        return self._tour_step

    @Property(int, constant=True)
    def tourCount(self) -> int:
        return len(DEMO_TOUR)

    @Property(bool, notify=changed)
    def reviewMode(self) -> bool:
        return self._review_mode

    @Property(int, notify=changed)
    def masteryLevel(self) -> int:
        return int(self._review_state["mastery_level"])

    @Property(str, notify=changed)
    def masteryLabel(self) -> str:
        return self._mastery_label(self.masteryLevel)

    @Property(str, notify=changed)
    def nextReviewText(self) -> str:
        due = str(self._review_state["due_date"])
        return f"Next review: {due}" if due else "Review schedule ready after completion"

    @Property(int, notify=changed)
    def bookmarkCount(self) -> int:
        return len(self.store.bookmarks())

    @Property("QStringList", notify=changed)
    def bookmarkItems(self) -> list[str]:
        return [f"{topic}  •  {title}" for topic, title in self.store.bookmarks()]

    @Slot(str)
    def selectTopic(self, topic: str) -> None:
        if topic not in LESSONS:
            return
        self._learning_goal = ""
        self._goal_position = 0
        self.store.set_learning_goal("")
        self.store.set_learning_goal_position(0)
        self._topic = topic
        self._lesson_index = self.store.lesson_index(topic) % len(LESSONS[topic])
        self._resume_topic = self._topic
        self._resume_lesson_index = self._lesson_index
        self._review_mode = False
        self._quiz_passed = False
        self._search_query = ""
        self.store.set_selected_topic(topic)
        self._load_lesson_tools()
        self.changed.emit()

    @Slot()
    def nextLesson(self) -> None:
        if self._review_mode:
            self._topic = self._resume_topic
            self._lesson_index = self._resume_lesson_index
            self._review_mode = False
        elif self._learning_goal:
            sequence = LEARNING_GOALS[self._learning_goal]
            self._goal_position = (self._goal_position + 1) % len(sequence)
            topic, title = sequence[self._goal_position]
            lesson_index = self._find_lesson(topic, title)
            if lesson_index is not None:
                self._topic = topic
                self._lesson_index = lesson_index
                self._resume_topic = topic
                self._resume_lesson_index = lesson_index
                self.store.set_learning_goal_position(self._goal_position)
                self.store.set_selected_topic(topic)
        else:
            self._lesson_index = (self._lesson_index + 1) % len(LESSONS[self._topic])
            self._resume_topic = self._topic
            self._resume_lesson_index = self._lesson_index
        self.store.set_lesson_index(self._topic, self._lesson_index)
        self._quiz_passed = False
        self._load_lesson_tools()
        self.changed.emit()

    @Slot(result=bool)
    def toggleBookmark(self) -> bool:
        lesson = self._lesson()
        self._bookmarked = not self._bookmarked
        self.store.set_bookmarked(lesson.topic, lesson.title, self._bookmarked)
        self.changed.emit()
        self.celebration.emit(
            "Lesson bookmarked." if self._bookmarked else "Bookmark removed."
        )
        return self._bookmarked

    @Slot(int)
    def openBookmark(self, index: int) -> None:
        bookmarks = self.store.bookmarks()
        if index < 0 or index >= len(bookmarks):
            return
        topic, title = bookmarks[index]
        self._open_lesson(topic, title, clear_goal=True)

    @Slot(int)
    def removeBookmark(self, index: int) -> None:
        bookmarks = self.store.bookmarks()
        if index < 0 or index >= len(bookmarks):
            return
        topic, title = bookmarks[index]
        self.store.set_bookmarked(topic, title, False)
        self._load_lesson_tools()
        self.changed.emit()
        self.celebration.emit("Bookmark removed.")

    @Slot(str)
    def saveLessonNote(self, note: str) -> None:
        lesson = self._lesson()
        self.store.save_lesson_note(lesson.topic, lesson.title, note)
        self._lesson_note = self.store.lesson_note(lesson.topic, lesson.title)
        self.changed.emit()
        self.celebration.emit(
            "Learning takeaway saved."
            if self._lesson_note
            else "Learning takeaway cleared."
        )

    @Slot(int)
    def openNote(self, index: int) -> None:
        notes = self.store.notes()
        if index < 0 or index >= len(notes):
            return
        topic, title, _ = notes[index]
        self._open_lesson(topic, title, clear_goal=True)

    @Slot(int)
    def removeNote(self, index: int) -> None:
        notes = self.store.notes()
        if index < 0 or index >= len(notes):
            return
        topic, title, _ = notes[index]
        self.store.save_lesson_note(topic, title, "")
        self._load_lesson_tools()
        self.changed.emit()
        self.celebration.emit("Learning takeaway removed.")

    @Slot(str)
    def selectLearningGoal(self, goal: str) -> None:
        if goal not in LEARNING_GOALS:
            return
        self._learning_goal = goal
        self._goal_position = 0
        self.store.set_learning_goal(goal)
        self.store.set_learning_goal_position(0)
        topic, title = LEARNING_GOALS[goal][0]
        self._open_lesson(topic, title)
        self.celebration.emit("Guided learning path started.")

    @Slot(str, result=str)
    def createCustomLearningPath(self, request: str) -> str:
        """Match prepared demo requests, or safely queue an unavailable topic."""
        clean_request = " ".join(request.strip().split())[:240]
        if len(clean_request) < 5:
            return "ERROR|Describe the subject in a few more words."

        normalized = clean_request.casefold()
        investment_terms = (
            "alternative investment",
            "portfolio",
            "private equity",
            "private credit",
            "hedge fund",
            "real asset",
            "diversification",
        )
        governance_terms = (
            "risk",
            "decision making",
            "bcbs",
            "data governance",
            "human in the loop",
            "human-in-the-loop",
            "issue management",
            "error management",
            "legal obligation",
            "impact assessment",
            "reporting governance",
        )

        if any(term in normalized for term in investment_terms):
            goal = "Understand alternative investments"
        elif any(term in normalized for term in governance_terms):
            goal = "Navigate risk and governance decisions"
        else:
            created = self.store.submit_topic_request(clean_request)
            message = (
                "Topic request saved locally. A connected release can notify you when a reviewed path is available."
                if created
                else "That topic is already in your request list."
            )
            return f"REQUESTED|{message}"

        self.selectLearningGoal(goal)
        return f"STARTED|{goal}"

    @Slot(str, result=bool)
    def openPreparedLearningTopic(self, subject: str) -> bool:
        prepared = PREPARED_LEARNING_TOPICS.get(subject)
        if prepared is None:
            return False
        goal, topic, title = prepared
        sequence = LEARNING_GOALS[goal]
        try:
            position = sequence.index((topic, title))
        except ValueError:
            return False
        self._learning_goal = goal
        self._goal_position = position
        self.store.set_learning_goal(goal)
        self.store.set_learning_goal_position(position)
        if not self._open_lesson(topic, title):
            return False
        self.celebration.emit(f"{subject} is ready.")
        return True

    @Slot(str)
    def selectTopLearningItem(self, item: str) -> None:
        if item in PREPARED_LEARNING_TOPICS:
            self.openPreparedLearningTopic(item)
        else:
            self.selectTopic(item)

    @Slot()
    def clearLearningGoal(self) -> None:
        self._learning_goal = ""
        self._goal_position = 0
        self.store.set_learning_goal("")
        self.store.set_learning_goal_position(0)
        self.changed.emit()
        self.celebration.emit("Guided learning path cleared.")

    @Slot(bool)
    def setReducedMotion(self, enabled: bool) -> None:
        self._reduced_motion = bool(enabled)
        self.store.set_reduced_motion(self._reduced_motion)
        self.changed.emit()

    @Slot(int, int)
    def saveWindowPosition(self, x: int, y: int) -> None:
        self.store.set_window_position(x, y)

    @Slot()
    def completeWelcome(self) -> None:
        if self._welcome_seen:
            return
        self._welcome_seen = True
        self.store.set_welcome_seen(True)
        self.changed.emit()

    @Slot()
    def nextDiscovery(self) -> None:
        self._discovery_offset = (self._discovery_offset + 1) % len(DISCOVERY_ITEMS)
        self.changed.emit()

    @Slot(str)
    def searchLessons(self, query: str) -> None:
        self._search_query = query[:80]
        self.changed.emit()

    @Slot(int)
    def openSearchResult(self, index: int) -> None:
        results = self._search_results()
        if 0 <= index < len(results):
            topic, title = results[index]
            self._open_lesson(topic, title, clear_goal=True)

    @Slot()
    def resetTour(self) -> None:
        self._tour_step = 0
        self.changed.emit()

    @Slot()
    def nextTour(self) -> None:
        if self._tour_step < len(DEMO_TOUR) - 1:
            self._tour_step += 1
            self.changed.emit()

    @Slot()
    def previousTour(self) -> None:
        if self._tour_step > 0:
            self._tour_step -= 1
            self.changed.emit()

    @Slot(result=str)
    def resetDemoData(self) -> str:
        reduced_motion = self._reduced_motion
        backup = self.store.reset_demo_data()
        self._topic = "AWS & Cloud"
        self._lesson_index = 0
        self._resume_topic = self._topic
        self._resume_lesson_index = 0
        self._learning_goal = ""
        self._goal_position = 0
        self._discovery_offset = 0
        self._search_query = ""
        self._tour_step = 0
        self._quiz_passed = False
        self._review_mode = False
        self._xp = 0
        self._streak = 0
        self._reduced_motion = reduced_motion
        self._welcome_seen = False
        if reduced_motion:
            self.store.set_reduced_motion(True)
        self._load_lesson_tools()
        self.changed.emit()
        self.celebration.emit("Demo reset complete. Your previous data was backed up.")
        return str(backup)

    @Slot(str)
    def setConfidence(self, confidence: str) -> None:
        if confidence not in {"got_it", "need_practice", "review_later"}:
            return
        lesson = self._lesson()
        self.store.set_confidence(lesson.topic, lesson.title, confidence)
        self._load_lesson_tools()
        self.changed.emit()

    @Slot(int)
    def checkAnswer(self, answer: int) -> None:
        lesson = self._lesson()
        expected = lesson.recall_answer if self._review_mode else lesson.answer
        explanation = (
            lesson.recall_explanation if self._review_mode else lesson.explanation
        )
        self._quiz_passed = answer == expected
        if self._review_mode and not self._quiz_passed:
            self.store.record_review_result(lesson.topic, lesson.title, False)
            self._load_lesson_tools()
        self.changed.emit()
        if self._quiz_passed:
            self.quizResult.emit(f"Correct — {explanation}", True)
        else:
            self.quizResult.emit("Not quite. Review the scenario and try again.", False)

    @Slot(result=bool)
    def completeLesson(self) -> bool:
        lesson = self._lesson()
        if not self._quiz_passed:
            self.celebration.emit("Answer the knowledge check first.")
            return False
        if self._review_mode:
            self.store.record_review_result(lesson.topic, lesson.title, True)
            awarded = self.store.complete(lesson.topic, f"{lesson.title} • Recall", 10)
            self._xp, self._streak = self.store.totals()
            self._load_lesson_tools()
            self.changed.emit()
            self.celebration.emit(
                (
                    f"+10 XP — mastery is now {self.masteryLabel}."
                    if awarded
                    else f"Recall strengthened — mastery is {self.masteryLabel}."
                )
            )
            return True
        if self.store.complete(lesson.topic, lesson.title, lesson.xp):
            self.store.set_confidence(lesson.topic, lesson.title, "review_later")
            self._xp, self._streak = self.store.totals()
            self._load_lesson_tools()
            self.changed.emit()
            self.celebration.emit(f"+{lesson.xp} XP — learning complete!")
        else:
            self.celebration.emit("This flash is already complete today.")
        return True
