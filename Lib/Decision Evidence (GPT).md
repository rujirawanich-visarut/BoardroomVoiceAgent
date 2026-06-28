# Decision Evidence and Backpressure Matrix for BoardroomVoiceAgent

## 1. Audited Pattern Library Change Log  
- **General:** Added authoritative framework citations (COSO, ISO, NIST, DOJ) to ground each pattern’s evidence requirements. Clarified terms (e.g. “trade-offs”, “risk appetite”). Removed ambiguous or unsupported phrasing (e.g. blanket *“win-win”* claims) and noted where human judgment is needed.  
- **Pattern-Specific:**  Each pattern entry now specifies required analysis (e.g. market research, ROI modeling, legal review) and key roles (CEO, CFO, CISO, Board, etc.) using best-practice sources. We flagged gaps (e.g. missing compliance checks) that would trigger semantic backpressure, and differentiated them from minor issues (repairable). Examples of faulty reasoning (*“certainty theater”*, *“fake win-win”*, and over-automated suggestions) were added based on decision-science and governance literature.  

## 2. Decision Evidence Matrix

| **Pattern** | **Real Decision Indicators** | **Informational-Only** | **Min. Evidence Before Commitment** | **Quantitative Evidence** | **Qualitative Evidence** | **Explicit Criteria** | **Material Assumptions** | **Accountable Roles** | **Governance/Approval** | **Compliance/Safety Boundaries** | **Backpressure Gaps** | **Fallback Triggers** | **Deterministic Repair** | **Decision Safe Now** | **Decision Not Yet Safe** | **Next Evidence Action** | **Certainty Theater Ex.** | **Fake Win-Win Ex.** | **Inappropriate Autonomy Ex.** | **Confidence & Jurisdiction** |
| :- | :- | :- | :- | :- | :- | :- | :- | :- | :- | :- | :- | :- | :- | :- | :- | :- | :- | :- | :- | :- |
| **P1: Market Expansion** | Committing budget to enter a specific new market; setting target market share. | General queries about market trends or routine sales data. | Market research (size, growth), competitive analysis (Porter’s Five Forces), regulatory review, financial models (NPV, cash flow). | Forecasted revenue lift, costs, ROI, market size. | Customer demand evidence, partner capabilities, cultural/regulatory context. | Minimum acceptable ROI or payback; target market share or growth threshold. | Current market growth continues; local operations can be established. | CEO (strategy), CFO (finance), business-unit head, local advisors. | Board/strategy committee sign-off for major expansions; possibly shareholder approval if large. | International trade laws, local regulations, anti-bribery (FCPA/UKBA) if foreign; currency risk. | No demand forecast or ROI; no risk assessment (currency, political); missing legal/regulatory review. | Ambiguous request format or missing company data (model/schema failure). | Questions or data errors (e.g. missing market data) can be fixed by gathering reports. | Pilot project in a small sub-market (test new channel). | Greenlight full launch without local validation (unsafe). | Commission detailed market study; consult legal counsel on local regulations. | *“We know for sure we’ll double sales by next year.”* | *“This expansion is a win-win – customers love our product *and* revenues skyrocketing with zero risk.”* | *Agent says “Expand now globally” without any analysis or human oversight.* | **Confidence:** Moderate. (Sources focus on general strategy – local market conditions vary.) **Jurisdiction:** Consider US/EU corporate norms; foreign expansion may need specific country guidance. |
| **P2: Portfolio Restructuring (M&A)** | Proposal to acquire, merge with, or divest a business unit; committing large capital or equity stake. | High-level strategy talk about growth or divestment trends. | Comprehensive due diligence (financials, liabilities, contracts); antitrust/regulatory risk analysis; integration plan or sale strategy. | Valuation models (DCF, multiples); synergy/cost-savings estimates; deal financing terms. | Target’s market position, management culture, ESG/ethical compliance. | Acceptable price range; post-deal capital structure; regulatory approval conditions. | Sufficient capital availability; target’s projections are reliable; post-merger synergy will materialize. | CEO/Corp Dev (lead M&A); CFO (valuation); General Counsel (legal); Board oversight (major deals). | Board approval required (often unanimous); in public companies, often shareholder consent (see ICLG M&A laws). | Antitrust clearance, foreign investment approval (CFIUS in US, EU Merger Regulation). | Missing financials, unclear funding plan, no regulatory strategy, lack of integration/resolution plan. | Incomplete or malformed financial model/schema. | Additional due diligence, revise financial model, hire advisors. | Continue existing operations; perhaps smaller pilot JV. | Closing deal before full due diligence (unsafe). | Engage external M&A advisors; complete regulatory filings; perform deep compliance audit. | *“They meet all our needs; let’s ignore the fine print.”* | *“Buy them, and everyone (employees, customers, shareholders) will only benefit with nothing to lose.”* | *Agent blithely recommends the merger without citing risks or requiring human approval.* | **Confidence:** Moderate. (Due-diligence practices are standard, but local regulatory thresholds vary.) **Jurisdiction:** US/UK law (Caremark duties) and regulators (DOJ/FTC in US, ECCP guidelines). |
| **P3: Strategic Partnership (Alliances/JV)** | Committing resources or signing a long-term alliance/JV agreement. | Exploratory partnership talks without commitment. | Mutual due diligence: strategic fit, cultural compatibility, financial health, legal contracts, exit clauses. | Joint venture financial projections; capital contributions; cost/benefit sharing models. | Partner’s reputation and integrity; goal alignment; governance model clarity. | Clear definition of partnership goals and KPIs; decision rights; exit terms. | Partner will honor commitments; synergies materialize; no hidden conflicts. | CEO/BDO (negotiation lead); CFO (joint financials); Legal (contracts); Board input on governance. | Board or authorized committee sign-off; potential antitrust review if JV large. | Foreign investment rules (e.g. national security review) if JV involves sensitive tech or countries. | No clear governance structure (roles, dispute resolution); no exit strategy; lack of performance metrics. | Incomplete context or mismatched data input. | Clarify objectives; refine partnership scope; re-engage with partner for details. | Continue current operation; perhaps smaller pilot collaboration. | Signing final JV contract without agreed governance (unsafe). | Conduct alignment workshops; draft governance charter; involve neutral mediator. | *“Trust me, they’ll do their part; details don’t matter.”* | *“This joint venture is a 100% win – full profit *and* full innovation with zero trade-off.”* | *AI suggests a partner solely based on keyword matching, ignoring culture/fit.* | **Confidence:** Moderate. (Guide assumes general JV best practices; actual risks vary by sector.) **Jurisdiction:** UAE/EU context (source), but principles apply broadly. |
| **P4: Capital Project Approval** | Committing major capex (e.g. plant/building) and timeline. | Seeking information on options or design without final decision. | Business case with cost-benefit (NPV/IRR), engineering feasibility, risk assessment, regulatory clearances, environmental impact study. | Cost breakdown, projected revenues/efficiencies, ROI metrics, sensitivity analyses. | Alignment with strategy, stakeholder buy-in, sustainability impacts. | Required ROI or payback period; environmental/regulatory compliance. | Budgeted funding is available; cost estimates accurate; demand projections hold. | CFO/Finance (cost approval), COO/Engineering (technical feasibility), CEO (strategy), Board (major projects). | Often Board or investment committee approval; for public projects may need government or bondholder approvals. | Permitting (zoning, safety codes), environmental laws (EPA, EU EIA directives), labor/safety regs (OSHA). | No engineering feasibility or capital budget; missing permits review; no contingency for overruns. | If cost models or data fail to load. | Fix spreadsheet errors; get updated cost quotes. | Perform additional analysis (value-engineering) on a portion of project. | Green-light full build without site survey or budget lock-down. | Commission independent feasibility study; engage legal on permits; re-validate cost estimates. | *“Everything is under control; costs won’t change.”* | *“We can build this plant at half the cost and it’ll solve all our resource problems.”* | *Autonomous agent directly issues construction orders without human oversight.* | **Confidence:** Moderate. (Capital project practices are universal, but costs/regulations vary by country.) **Jurisdiction:** US/EU construction and environmental law. |
| **P5: Budget & Prioritization** | Allocating budget across projects or departments to meet strategic goals. | Reviewing past budgets or preliminary forecasts (no commitment). | Financial forecasts vs targets, project ROI analyses, risk assessments (COSO/ERM approach). | Budget vs actual figures, ROI, cost-benefit for each option, revenue forecasts. | Strategic importance of initiatives, organizational capacity, stakeholder impacts. | Alignment to strategic priorities; minimum performance metrics. | Forecasts are realistic; no sudden cost shocks; economic conditions stable. | CFO (budget owner), CEO, Business Unit heads, Budget Committee. | Board oversight of overall budgets, especially CapEx vs Opex trade-offs. | Financial reporting regulations (GAAP/IFRS), funding constraints, covenant limits. | Missing ROI comparisons or unclear strategic fit of items; lack of contingency buffer. | If data tables or financial model schema fail. | Obtain updated forecasts, re-run models, correct input data. | Approve small discretionary budgets (safe incremental funding). | Deferring budget review altogether (unsafe). | Have each department submit clear business cases; hold budget review sessions. | *“We know these projects will all pay off, so approve everything as is.”* | *“We can do all of this on the existing budget and everyone’s happy – zero downsides.”* | *“Auto-generator says fund every request at 100%.”* | **Confidence:** Moderate. (General ERM guidance used; specific financial rules vary.) **Jurisdiction:** Standard corporate accounting practices (IFRS/GAAP) apply globally. |
| **P6: Pricing Strategy** | Setting new product/service prices or pricing tiers. | Market or competitor pricing info without changing price. | Cost analysis (floor price), customer value research (ceiling price), competitor price benchmarking, demand elasticity studies. | Cost of goods sold, margin targets, elasticity metrics, competitor prices. | Customer willingness-to-pay, brand positioning, competitive dynamics. | Price floor (cover costs) and ceiling (max perceived value). | Production/distribution costs, market demand, competitor actions remain as assumed. | CMO/Marketing (market input), CFO (margin analysis), Sales (field feedback), Legal (pricing regulations). | Legal oversight for anti-trust (collusion) or regulated industries (utilities); Board typically reviews major pricing changes for key products. | Antitrust/competition law; price discrimination rules (e.g. Robinson-Patman in US), export pricing regulations. | No clear cost breakdown; no customer willingness data; ignoring regulatory price limits. | If algorithmic pricing model fails or incomplete data. | Fix dataset; rerun pricing model. | Conduct a limited market test with new price. | Roll out price change company-wide without testing. | Gather market survey on price sensitivity; revise pricing model. | *“Trust me, demand is inelastic so raise prices arbitrarily.”* | *“This new price will delight customers and also increase our margin perfectly.”* | *Agent automatically sets price equal to highest competitor’s without rationale.* | **Confidence:** Moderate. (Consumer value theory and costs are cited; local pricing laws vary.) **Jurisdiction:** Competition laws differ (EU vs US Sherman Act) and sector regulation. |
| **P7: Growth vs. Profit Trade-off** | Shifting focus between revenue growth initiatives and profitability targets. | Discussing growth or profit metrics in isolation without a concrete decision. | Scenario analysis of marginal revenue vs marginal cost, impact on EBITDA, capacity limits. | Growth projections, cost projections, EBITDA margins, margin sensitivity. | Market saturation risk, organizational capacity, risk of debt/leveraging. | Sustainable growth rate (e.g. revenue growth > cost growth). | Market demand holds; cost structure scalable. | CFO (financial modeling), CEO (strategy), Board (risk appetite setting). | Board defines risk appetite (growth vs profitability); possibly investor approvals if strategy changes drastically. | Debt covenants, liquidity requirements, viability of business model. | Missing sensitivity analysis; no clear risk tolerance (gap in risk appetite). | Model computation errors. | Re-calibrate forecasts; correct input assumptions. | Adjust investment pace (incremental growth push). | Aggressively cut costs without revenue plan. | Run scenario tests for different growth/cost rates. | *“We will grow 50% this year with no extra costs!”* | *“We can maximize both growth and profits without any trade-offs – everyone wins!”* | *AI suggests unlimited growth spending ignoring margin impacts.* | **Confidence:** Moderate. (Basic economic principle cited; actual thresholds are company-specific.) **Jurisdiction:** Universal economic logic; local market factors must be judged by human experts. |
| **P8: Supply Chain Resilience** | Decisions on supplier diversification, inventory buffers, or contingency plans. | Routine inventory monitoring or vendor performance reports. | Supply chain risk assessment (identifying single points of failure); inventory metrics; scenario stress-tests. | Lead time variability, fill rates, cost of disruptions, backup capacity. | Supplier reliability, geopolitical/ESG risks, supply chain visibility. | Contingency/flexibility metrics (e.g. alternate suppliers, safety stock). | Global supply conditions; transportation networks functioning. | Supply Chain/SCO, COO, Procurement; CFO (costs); Risk management team. | Board/risk committee oversight for critical supply (especially if strategic or regulated). | Regulation on trade, export controls, sanctions; critical infrastructure mandates. | No contingency plans; single-source suppliers unchecked; lack of demand-variance data. | Data feed errors (inventory system failure). | Update supplier databases; repair data pipelines. | Activate alternative sourcing plan immediately. | Committing to sole-source supplier indefinitely. | Perform supply chain stress simulation; seek alternate quotes. | *“Our supplier will never fail us, so we don’t need a backup.”* | *“This plan will keep everyone safe and profitable – no downside at all.”* | *Agent auto-orders full production ignoring current shortages.* | **Confidence:** Moderate. (IBM/industry best practices cited; local hazards (e.g. regional disasters) vary.) **Jurisdiction:** Global supply chain standards; critical industry regs (e.g. pharmaceuticals) may apply regionally. |
| **P9: Operational Safety/Compliance** | Decisions to implement safety systems, compliance programs, or major process changes. | Updates on safety training attendance or compliance checklists without commitment. | Hazard assessment results, safety audits, compliance program reviews, legal exposure analysis. | Incident rate statistics, compliance audit scores, fine exposure estimates. | Safety culture maturity, management commitment, workforce feedback. | Regulatory compliance standards must be met; target incident reduction goals. | Existing safety programs are effective; risk mitigations cover all major hazards. | Safety Officer/EHS Manager; COO/Operations; Legal; CEO (for safety culture). | Board/audit committee oversight of major compliance (often via safety/regulatory committees). | OSHA standards (US) or local equivalent; industrial safety laws (e.g. machinery directives EU). | Absence of risk assessments or incident analyses; no legal compliance audit (gap in safety controls). | If safety data feed or audit reports fail to load. | Re-run risk assessment; fix data collection. | Temporarily implement extra safeguards (e.g. stricter PPE) while auditing. | Proceed without safety review (unsafe). | Commission external safety audit; remediate immediate hazards. | *“We’ve never had an accident, so we don’t need to do anything.”* | *“We’ll cut safety training and still be 100% compliant and efficient.”* | *Agent advises ignoring a new OSHA rule change.* | **Confidence:** High. (OSHA core elements cited apply widely in regulated industries.) **Jurisdiction:** Local occupational safety laws (OSHA US, EU PUWER, etc.); vary by country/industry. |
| **P10: Technology Adoption (Digital/AI)** | Commitment to invest in new tech platforms (e.g. ERP, AI system) or retire old systems. | Gathering vendor info or doing tech demos (no purchase decision). | Cost-benefit analysis, integration impact study, cybersecurity review, ROI projections. | Total cost of ownership vs projected efficiency gains or revenue impact. | Employee readiness, change management factors, alignment to business processes. | Expected ROI threshold, compatibility with legacy systems. | Tech will be delivered on time/budget, employees adopt change. | CIO/CTO (tech fit), CFO (ROI), CISO (security), COO. | Board approval for large IT investments (often via IT committee); audit on IT controls (COBIT frameworks). | Data privacy/compliance (e.g. GDPR if personal data used); cybersecurity standards (NIST CSF integration). | Unproven ROI model; missing data on current process inefficiencies; ignored security implications. | If the AI or tech demo crashes or integration schema fails. | Gather pilot metrics; refine requirements. | Start with pilot deployment or MVP. | Full roll-out without pilot testing or security review (unsafe). | Run a small proof-of-concept; involve end-users for feedback. | *“Just buy the tool; it solves all our problems automatically.”* | *“Implementing this AI will both double productivity and boost morale simultaneously.”* | *AI tool alone decides full migration without oversight.* | **Confidence:** Moderate. (General best-practices used; tech ROI and risks differ by context.) **Jurisdiction:** Tech standards (ISO 27001, GDPR) and industry-specific IT governance vary by region. |
| **P11: Cybersecurity Investment** | Committing budget or policies to enhance security (e.g. buy firewall, hire CISO). | General security updates or runbooks (no new policy change). | Formal risk assessment (loss estimation), gap analysis against NIST CSF or similar; business impact analysis. | Potential breach cost models, ROI of controls (CISO often uses value-at-risk). | Threat landscape understanding, maturity of security culture, legal exposure. | Risk appetite for cyber incidents (e.g. downtime tolerance); minimum security standards (e.g. ISO/IEC 27001). | Current controls will mitigate top risks; threat environment remains within forecasts. | CISO or Security Lead; CIO; CEO (ultimate accountability); Audit Committee. | Often overseen by Board’s risk or audit committee; possibly specific regulations (SOX, GLBA). | Data breach notification laws, sector regulations (HIPAA, PCI-DSS), fiduciary duty (Board oversight expectations). | No threat/risk model presented; missing patch management/incident response plan; no reporting to board. | If security scanning tool or threat data feed fails. | Run manual assessment; reboot tools. | Increase monitoring (but don’t commit major changes yet). | Major investment (e.g. new security platform) without clear risk rationale. | Initiate a third-party pen-test or audit. | *“Our systems are unhackable, so invest nothing.”* | *“This security solution will stop every attack and cost nothing.”* | *AI decides security configuration without human review.* | **Confidence:** High. (Expert legal alert explicitly states board’s role; best practices align with NIST CSF.) **Jurisdiction:** US board duties (Delaware Caremark) and regulatory regimes (e.g. SEC cybersecurity rules) apply; similar concepts in EU (e.g. GDPR, NIS Directive). |
| **P12: Data Privacy/Use** | Deciding on data collection/use (e.g. launching AI using customer data) or new privacy policies. | Reporting data metrics or past compliance status (no policy change). | Data mapping & Privacy Impact Assessment (GDPR DPIA), legal review of applicable privacy laws. | Number of data subjects impacted, potential fines, compliance audit results. | Customer sentiment, ethical considerations, data governance maturity. | Consent requirements and data minimization standards; regulatory limits (e.g. CCPA opt-outs). | Data processing is lawful; no new high-risk categories introduced. | Chief Privacy Officer/Data Protection Officer; Legal; CIO; Board oversight for strategy. | Must comply with privacy laws (GDPR, CCPA, ePrivacy) and industry rules (HIPAA for health, FINRA for finance). | Breach of GDPR/CPRA (substantial fines, e.g. FTC algorithmic model removal). | Lack of DPIA or legal review, undefined data classification; missing accountability (who owns data use?). | If data schemas or consent records are unavailable. | Conduct manual legal review; fix data mappings. | Delay new data use until audit. | Launching AI on data without consent or impact analysis. | Draft and approve a clear data governance policy. | *“We’ll just anonymize, so regulations don’t apply.”* | *“Using this consumer data benefits everyone with zero privacy risk.”* | *AI autonomously profiles customers and acts on personal data without oversight.* | **Confidence:** High. (Harvard CorpGov analysis stresses board role and evolving laws.) **Jurisdiction:** Privacy law varies: GDPR/EU vs state laws (CCPA) vs sector laws; guidance must be localized. |
| **P13: Regulatory Compliance** | Deciding on compliance program changes or responses to new laws. | Reviewing compliance reports or hotline stats without action. | Compliance risk assessment (e.g. FCPA exposure, SOC reports), audit findings, legal/regulatory interpretations. | Number of identified violations, cost of non-compliance fines, audit ratings. | Organizational tone, ethical culture, precedent cases. | Compliance with relevant laws (e.g. Anti-bribery, environmental); internal control adequacy. | Compliance costs vs business benefit; regulators’ enforcement stance. | Chief Compliance Officer (CCO); Legal Counsel; CEO; Board (often Audit or Compliance Committee). | Board oversight mandated by law (Delaware Caremark duty); DOJ/SEC guidelines (ECCP encourages board access to CCO). | No escalation mechanism; incomplete policies in key risk areas (e.g. anti-corruption, data protection). | If training LMS or compliance data system fails. | Update policies; retrain staff; fix systems. | Rectify minor policy (e.g. update a form). | Operating unaware of new regulation (unsafe). | Conduct compliance gap analysis; engage outside counsel. | *“Our policy is enough; we don’t need audits.”* | *“We can cut compliance budget and still be fully protected.”* | *Agent says we should auto-publish unreviewed data claiming “good for transparency.”* | **Confidence:** High. (Legal theory and DOJ guidance cited.) **Jurisdiction:** U.S. corporate law (Caremark, DOJ ECCP); other countries have similar expectations (e.g. UK Senior Managers Regime). |
| **P14: Risk Appetite/Strategy** | Setting or changing the company’s overall risk appetite or tolerance. | Discussing general risk concerns without formal limits. | Board-approved risk appetite statement (per ISO 31000/ERM); analysis linking risk to strategy (COSO ERM). | Capital-at-risk, stress-test results, risk-reward trade-off metrics. | Strategic priorities, stakeholder expectations, market volatility. | Explicit risk appetite levels (e.g. credit risk limits, volatility tolerance). | Future market conditions follow forecasts; risk modeling assumptions hold. | Board of Directors (ultimately responsible); Risk Committee, CFO/CRO. | Usually board policy document; any change often requires full board vote (fiduciary duty). | Regulatory capital requirements (banks, insurers have mandated risk policies), ESG or safety risk caps. | No documented risk appetite; no linkage of strategy choices to risk capacity. | If risk model or scoring system breaks. | Update risk models; recalc with new inputs. | Minor recalibration of existing appetite (e.g. adjust one threshold). | Shifting to high-leverage strategy without appetite review. | Hold a board session to explicitly approve risk limits. | *“Take every project on; we’re going 100% growth.”* | *“We can both be completely safe and 10x our returns – no trade-offs.”* | *AI auto-allocates resources ignoring risk limits.* | **Confidence:** Moderate. (ISO definitions used; actual risk tolerance determination requires judgement and context.) **Jurisdiction:** Finance regulators often specify risk policies; general corporate use guided by COSO/ISO. |
| **P15: Org & Workforce Strategy** | Decisions on hiring, restructuring, reskilling, or DEI initiatives. | HR reports on turnover or headcount without action. | HR analytics (turnover rates, skill gaps) and strategic workforce planning (linking to business goals). | Employee engagement scores, turnover rates, diversity metrics, training ROI. | Culture and morale, leadership pipeline strength, external labor market trends. | Targets for talent metrics (diversity, retention); strategic alignment of roles. | Skills demand by strategy remains as planned; current HR programs scale. | CHRO/HR Director; CEO; Board (often Remuneration/People & Culture Committee). | Governance may involve a Board-level HR or People committee; labor law constraints (union deals). | Employment laws, OSHA (for workforce safety), shareholder/stakeholder expectations (e.g. ESG reporting on human capital). | No analysis of skill gaps or DEI metrics; no link to strategy (gap in human capital planning). | If data (e.g. LMS/training system) fails. | Re-survey employees; patch incomplete data. | Begin small pilot of training program. | Announce massive hiring freeze without plan. | Collect employee survey data; update org chart. | *“We’ll hire everyone who applies; more people = better outcomes.”* | *“We can be fully inclusive, double productivity, and halve costs at the same time.”* | *Agent restructures org chart without human guidance.* | **Confidence:** Moderate. (Governance articles cited; specifics depend on culture/regulations.) **Jurisdiction:** Labor laws (US at-will vs EU works councils), corporate governance codes (e.g. Japan’s Stewardship Code) differ by country. |

## 3. JSON-Compatible Decision Evidence Matrix  
```json
[
  {
    "pattern_id": "P1",
    "real_decision_indicators": ["Allocating budget to enter new market","Setting target market share"],
    "info_indicators": ["General market trend queries","Pilot study reviews (not commitment)"],
    "min_evidence": ["Market research data","Competitive analysis (Porter)","Regulatory/legal review","Financial forecasts"],
    "quantitative_evidence": ["Revenue/cost forecasts","ROI/NPV calculations","Market size metrics"],
    "qualitative_evidence": ["Customer demand insights","Competitive landscape","Regulatory context","Corporate strategy alignment"],
    "explicit_criteria": ["Target ROI or payback period","Growth vs. margin balance","Market share goals"],
    "material_assumptions": ["Demand growth continues","No unforeseen regulatory changes","Market environment stable"],
    "accountable_roles": ["CEO (strategy)","CFO (financials)","Business Unit Director","Legal Counsel"],
    "governance_boundaries": ["Board approval for major expansion","Shareholder vote if significant","Investment committee review"],
    "safety_legal_boundaries": ["Foreign investment regulations","FCPA/anti-bribery laws","Trade agreements/tariffs"],
    "backpressure_gaps": ["No demand forecast","Unclear ROI comparison","Missing risk assessment","Unvetted regulatory analysis"],
    "fallback_triggers": ["Data/model loading error","Ambiguous request phrasing"],
    "repairable_issues": ["Minor data entry errors","Additional market reports can be obtained"],
    "decision_safe_now": ["Authorize small pilot project","Allocate funds for further research"],
    "decision_not_safe": ["Major rollout without validation","Full commitment without detailed plan"],
    "next_evidence_action": ["Commission detailed market study","Engage legal/regulatory advisor","Pilot customer surveys"],
    "certainty_theater_examples": ["\"This new country is guaranteed to double sales.\""],
    "fake_win_win_examples": ["\"Expansion will only improve profits and brand image with no trade-offs.\""],
    "auto_recommendation_examples": ["\"Agent suggests full launch without citing any constraints.\""],
    "confidence": "Moderate (depends on market-specific data reliability)",
    "jurisdiction": "General corporate context; specific international expansion rules vary by country."
  },
  {
    "pattern_id": "P2",
    "real_decision_indicators": ["Proposing M&A or divestiture","Committing acquisition budget"],
    "info_indicators": ["Discussion of strategic options","Initial target identification"],
    "min_evidence": ["Full due diligence (financial, legal, compliance)","Regulatory risk analysis","Integration/divestiture plan"],
    "quantitative_evidence": ["Valuation (DCF, multiples)","Synergy/cost-saving estimates","Deal financing structure"],
    "qualitative_evidence": ["Target’s strategic fit","Cultural compatibility","Reputation/ESG track record"],
    "explicit_criteria": ["Acceptable purchase price","Shareholder approval thresholds","Antitrust clearance prerequisites"],
    "material_assumptions": ["Target’s projections are accurate","Market conditions at closing remain stable","Deal synergies realized"],
    "accountable_roles": ["Chief Development Officer","CFO","General Counsel","Board of Directors"],
    "governance_boundaries": ["Board approval (often unanimous)","Shareholder vote for large deals","Audit Committee oversight"],
    "safety_legal_boundaries": ["Antitrust/competition law","Foreign investment (CFIUS etc.)","Corporate law (fiduciary duties)"],
    "backpressure_gaps": ["Incomplete financial data","No antitrust strategy","Lack of integration plan","Unassessed liabilities"],
    "fallback_triggers": ["Failure to retrieve target's data","Model computation error"],
    "repairable_issues": ["Missing detail in financials can be gathered","Legal questions clarified with counsel"],
    "decision_safe_now": ["Proceed with continued due diligence","Negotiate standstill agreements"],
    "decision_not_safe": ["Closing a deal with unresolved regulatory risk","Funding a takeover without terms agreed"],
    "next_evidence_action": ["Engage M&A consultants","Conduct compliance audits","Draft regulatory filing"],
    "certainty_theater_examples": ["\"They have identical products; acquisition is risk-free.\""],
    "fake_win_win_examples": ["\"Merging with them will solve all our problems and theirs without compromise.\""],
    "auto_recommendation_examples": ["\"Agent automatically approves the merger with no risk discussion.\""],
    "confidence": "Moderate (standard M&A process, but outcomes vary widely)",
    "jurisdiction": "US/UK law context; regulatory approvals differ by country (e.g. EU vs. US FTC)."
  },
  {
    "pattern_id": "P3",
    "real_decision_indicators": ["Signing alliance or JV agreement","Allocating shared resources to partnership"],
    "info_indicators": ["Exploratory partner meetings","RFP issuance for partnership"],
    "min_evidence": ["Mutual due diligence (strategic, financial, cultural)","Legal governance/exits defined","Strategic fit analysis"],
    "quantitative_evidence": ["Joint financial forecasts","Contribution of assets (cash, IP, R&D)","Cost-share models"],
    "qualitative_evidence": ["Cultural fit","Reputation/integrity of partner","Long-term alignment of goals"],
    "explicit_criteria": ["Shared objectives clearly stated","Governance and decision rights defined","Exit strategy defined"],
    "material_assumptions": ["Both parties commit resources as promised","Market synergies will materialize","Legal structures are sound"],
    "accountable_roles": ["CEO/Business Dev","CFO","General Counsel","Board oversight"],
    "governance_boundaries": ["Board approval for joint ventures","Audit/Risk Committee review","Required notification to regulators if applicable"],
    "safety_legal_boundaries": ["Competition law (if JV might affect markets)","Foreign JV approvals","Sanctions/embargoes check"],
    "backpressure_gaps": ["No clear governance framework","Missing exit terms","Unverified partner commitments","Undefined KPIs"],
    "fallback_triggers": ["Data alignment failure","Format/schema issues in proposal documents"],
    "repairable_issues": ["Clarify partnership scope","Adjust draft terms based on feedback"],
    "decision_safe_now": ["Develop detailed memorandum of understanding","Conduct pilot projects together"],
    "decision_not_safe": ["Formalizing JV without agreed operating model","Committing funds without signed agreements"],
    "next_evidence_action": ["Create joint governance charter draft","Perform background checks on partner","Engage JV consultants"],
    "certainty_theater_examples": ["\"They will keep their promises, so we don’t need details.\""],
    "fake_win_win_examples": ["\"This partnership is 100% beneficial to both sides with no trade-offs.\""],
    "auto_recommendation_examples": ["\"Agent automatically proposes a 50-50 JV with no analysis.\""],
    "confidence": "Moderate (due diligence guidance used; real-world fit must be judged case-by-case)",
    "jurisdiction": "General business context; international JV subject to national laws and trade rules."
  },
  {
    "pattern_id": "P4",
    "real_decision_indicators": ["Approving significant capital expenditure (plant, equipment)","Allocating long-term funds"],
    "info_indicators": ["Reviewing project options or preliminary designs"],
    "min_evidence": ["Business case with cost-benefit (NPV/IRR)","Engineering feasibility","Risk mitigation plan"],
    "quantitative_evidence": ["Projected cash flows","Cost estimates (materials, labor)","ROI/payback period"],
    "qualitative_evidence": ["Strategic alignment","Environmental impact","Stakeholder (community) response"],
    "explicit_criteria": ["Minimum ROI threshold","Budget limit","Environmental/regulatory compliance targets"],
    "material_assumptions": ["Cost estimates are accurate","Energy/resource prices remain stable","Permits will be granted as expected"],
    "accountable_roles": ["CEO","CFO","COO/Engineering","Board (for large projects)"],
    "governance_boundaries": ["Board or investment committee approval","Finance committee oversight","Audit review for capex projects"],
    "safety_legal_boundaries": ["Building codes","Environmental regulations (EIA)","Health/safety laws (OSHA/EU directives)"],
    "backpressure_gaps": ["No independent feasibility study","Missing regulatory permit analysis","No contingency budget"],
    "fallback_triggers": ["Spreadsheet/model error","Lack of data (e.g. supplier quotes)"],
    "repairable_issues": ["Update cost quotes","Fill missing financial info"],
    "decision_safe_now": ["Proceed with limited-phase execution","Order long-lead items after partial review"],
    "decision_not_safe": ["Full construction start without final plan","Cancelling required safety studies"],
    "next_evidence_action": ["Hire engineering consultants","File for necessary permits","Re-evaluate cost contingencies"],
    "certainty_theater_examples": ["\"Engineering says it’s easy, we’ll finish under budget for sure.\""],
    "fake_win_win_examples": ["\"This project will both save money and have zero delays with no added risk.\""],
    "auto_recommendation_examples": ["\"Agent instructs immediate build-out ignoring unresolved issues.\""],
    "confidence": "Moderate (project management best practices cited; specifics vary by industry)",
    "jurisdiction": "Subject to local construction and environmental law; consult local experts."
  },
  {
    "pattern_id": "P5",
    "real_decision_indicators": ["Finalizing budget allocations for next period","Setting funding priorities across projects"],
    "info_indicators": ["Collecting budget requests","Preliminary financial reporting"],
    "min_evidence": ["Cost-benefit analyses for initiatives","Historical budget performance","Risk-return alignment (COSO ERM)"],
    "quantitative_evidence": ["Projected revenues vs costs","Budget vs actual comparisons","ROI of funded projects"],
    "qualitative_evidence": ["Strategic importance","Capacity constraints","External market conditions"],
    "explicit_criteria": ["Strategic fit of expenditures","Minimum financial performance metrics","Risk exposure limits"],
    "material_assumptions": ["Economic environment remains stable","Current revenue forecasts are met"],
    "accountable_roles": ["CFO (budget owner)","CEO","Business Unit Heads","Board (oversight)"],
    "governance_boundaries": ["Board approves total capital envelope","Audit Committee reviews process"],
    "safety_legal_boundaries": ["Financial reporting standards (budget transparency)","Grant/funding covenants if any"],
    "backpressure_gaps": ["Unjustified line items","No risk adjustment in scenarios","Lack of contingency funds"],
    "fallback_triggers": ["Data integration failure","Missing input (e.g. last quarter figures)"],
    "repairable_issues": ["Correct data entry errors","Clarify vague budget requests"],
    "decision_safe_now": ["Allocate a conservative contingency","Defer discretionary spending"],
    "decision_not_safe": ["Full funding without ROI validation","Cross-the-board cuts without analysis"],
    "next_evidence_action": ["Refine financial projections","Request clarifications from BUs"],
    "certainty_theater_examples": ["\"Allocate full budget because ‘we always meet targets’.\""],
    "fake_win_win_examples": ["\"We can boost every project’s funding with no cuts needed.\""],
    "auto_recommendation_examples": ["\"Agent slashes costs arbitrarily without context.\""],
    "confidence": "Moderate (based on COSO ERM linking strategy; specifics are organizational).",
    "jurisdiction": "Applies generally across sectors; no special legal variations beyond standard financial regulations."
  },
  {
    "pattern_id": "P6",
    "real_decision_indicators": ["Setting or changing product/service prices","Approving pricing tiers or discounts"],
    "info_indicators": ["Analyzing competitor prices","Cost reports with no decision ask"],
    "min_evidence": ["Cost analysis (floor price)","Customer value/elasticity research","Competitive market study"],
    "quantitative_evidence": ["Cost of goods, margins","Price elasticity of demand","Sales volume projections"],
    "qualitative_evidence": ["Brand positioning","Customer willingness-to-pay","Market perception"],
    "explicit_criteria": ["Price floor (covers cost) and ceiling (perceived value)","Margin targets","Regulatory limits"],
    "material_assumptions": ["Costs remain as estimated","Competitors maintain current pricing"],
    "accountable_roles": ["CFO","CMO/Sales","Product Management","Legal"],
    "governance_boundaries": ["Board oversight for major pricing changes","Industry regulators (utilities)"],
    "safety_legal_boundaries": ["Antitrust/collusion laws","Price discrimination/regulation statutes"],
    "backpressure_gaps": ["No cost breakdown","Ignoring legal price controls","No customer survey data"],
    "fallback_triggers": ["Calculation errors","Data source unavailable"],
    "repairable_issues": ["Re-run pricing model","Update cost data"],
    "decision_safe_now": ["Test new price in pilot market","Implement gradual price change"],
    "decision_not_safe": ["Implement large price hike without analysis","Setting price below cost"],
    "next_evidence_action": ["Conduct customer surveys","Perform competitive price monitoring"],
    "certainty_theater_examples": ["\"We know customers won’t notice a price jump.\""],
    "fake_win_win_examples": ["\"This pricing strategy will increase sales and margin simultaneously with no trade-off.\""],
    "auto_recommendation_examples": ["\"Agent sets price equal to highest competitor, ignoring demand or cost.\""],
    "confidence": "Moderate (principles of pricing cited; outcomes market-specific).",
    "jurisdiction": "Competition law varies (EU vs US antitrust); regulated industries have price caps."
  },
  {
    "pattern_id": "P7",
    "real_decision_indicators": ["Choosing growth initiatives vs. cost-cutting","Rebalancing budget between expansion and margins"],
    "info_indicators": ["Reviewing current growth stats","Discussing general strategy"],
    "min_evidence": ["Business model analysis","Scenario planning of marginal revenue vs. cost"],
    "quantitative_evidence": ["Revenue growth rates","Cost growth rates","EBITDA margins"],
    "qualitative_evidence": ["Market saturation risk","Operational capacity","Competitive position"],
    "explicit_criteria": ["Sustainable growth condition (Marginal Revenue > Marginal Cost)","Risk tolerance thresholds"],
    "material_assumptions": ["Growth opportunities will continue","Cost structure remains controllable"],
    "accountable_roles": ["CFO","CEO","Business strategy team","Board of Directors"],
    "governance_boundaries": ["Board sets overall risk appetite","Investor expectations"],
    "safety_legal_boundaries": ["Financial solvency regulations (for lenders)","Disclosure obligations if guidance changes"],
    "backpressure_gaps": ["No analysis of cost elasticity","Missing capital availability check"],
    "fallback_triggers": ["Forecast model error","Ambiguous metric definitions"],
    "repairable_issues": ["Refine forecasting model","Clarify assumptions"],
    "decision_safe_now": ["Adjust one strategic lever (e.g. small marketing boost)","Pilot new product line modestly"],
    "decision_not_safe": ["Aggressive expansion with no margin plan","Cutting costs in revenue-critical areas without study"],
    "next_evidence_action": ["Perform sensitivity analysis on growth vs cost","Scenario workshops with leadership"],
    "certainty_theater_examples": ["\"We’ll grow 30% this year with only a tiny increase in costs.\""],
    "fake_win_win_examples": ["\"We can cut costs and boost growth without any sacrifice.\""],
    "auto_recommendation_examples": ["\"Agent increases budget on all projects equally without trade-off analysis.\""],
    "confidence": "Moderate (economic principle cited; context-dependent on industry).",
    "jurisdiction": "Broadly applicable concept; no specific legal jurisdiction constraints."
  },
  {
    "pattern_id": "P8",
    "real_decision_indicators": ["Reconfiguring supply chain (new suppliers, inventory policies)","Investing in resilience measures"],
    "info_indicators": ["Routine supply performance reports","External event monitoring"],
    "min_evidence": ["Supply chain risk assessment","Inventory/lead-time analysis","Contingency planning documentation"],
    "quantitative_evidence": ["Lead time variability","Safety stock levels","Switching cost estimates"],
    "qualitative_evidence": ["Supplier reliability","Geopolitical risk factors","Production flexibility"],
    "explicit_criteria": ["Contingency capacity metrics (e.g. backup suppliers)","Service level thresholds"],
    "material_assumptions": ["Global logistics remain stable","Key suppliers stay in business"],
    "accountable_roles": ["Supply Chain/Procurement Director","COO","Risk Manager","CFO (financial impact)"],
    "governance_boundaries": ["Board/risk committee oversight for critical supply","Audit of vendor management processes"],
    "safety_legal_boundaries": ["Trade compliance (export controls)","Critical infrastructure regulations"],
    "backpressure_gaps": ["Single-sourcing without backup","No scenario analysis for disruptions"],
    "fallback_triggers": ["Failure of data integration systems","Incomplete supply visibility"],
    "repairable_issues": ["Gather backup supplier info","Fill missing supply chain data"],
    "decision_safe_now": ["Implement a modest buffer stock","Negotiate alternative supplier on standby"],
    "decision_not_safe": ["Rely on sole supplier with no contingency","Ignoring known supply constraints"],
    "next_evidence_action": ["Run disruption simulations","Engage procurement in risk modeling"],
    "certainty_theater_examples": ["\"Nothing bad will happen, so no need to diversify.\""],
    "fake_win_win_examples": ["\"This new supplier will cut costs and boost resilience simultaneously.\""],
    "auto_recommendation_examples": ["\"AI auto-orders triple inventory without justification.\""],
    "confidence": "Moderate (supply chain literature cited; specifics like covid lessons apply contextually).",
    "jurisdiction": "Global context; industry-specific regulations (e.g. FDA for pharma supply) apply."
  },
  {
    "pattern_id": "P9",
    "real_decision_indicators": ["Changing safety protocols or major compliance programs","Investing in hazard control systems"],
    "info_indicators": ["Routine safety audit results","Incident rate statistics"],
    "min_evidence": ["Hazard identification/risk assessment","Safety audit findings","Regulatory gap analysis"],
    "quantitative_evidence": ["Incident frequencies","Compliance audit scores","Potential penalty estimates"],
    "qualitative_evidence": ["Safety culture maturity","Worker feedback","External safety benchmarks"],
    "explicit_criteria": ["Compliance with safety standards","Target incident reduction rates"],
    "material_assumptions": ["Existing controls are effective","Regulatory requirements stable"],
    "accountable_roles": ["EHS (Safety) Director","COO","General Counsel","CEO"],
    "governance_boundaries": ["Board/audit committee oversight of safety programs","Regulator inspections"],
    "safety_legal_boundaries": ["OSHA/EU safety directives","Industry-specific safety laws"],
    "backpressure_gaps": ["Missing risk assessments","No incident investigation reports","Outdated procedures"],
    "fallback_triggers": ["Failure of safety monitoring systems","Incomplete inspection data"],
    "repairable_issues": ["Correct missing log entries","Retest failed sensors"],
    "decision_safe_now": ["Address known hazards incrementally","Allocate immediate funds for urgent fixes"],
    "decision_not_safe": ["Ignoring known safety issues","Assuming compliance without checks"],
    "next_evidence_action": ["Commission external safety audit","Update training records"],
    "certainty_theater_examples": ["\"We’ve always been safe; we don’t need changes.\""],
    "fake_win_win_examples": ["\"Cut safety costs, productivity rises and risks magically vanish.\""],
    "auto_recommendation_examples": ["\"Agent disables safety checks to speed up production.\""],
    "confidence": "High (OSHA recommendations are well-established best practices).",
    "jurisdiction": "Subject to local OSH laws; regulatory details differ by country."
  },
  {
    "pattern_id": "P10",
    "real_decision_indicators": ["Investing in new technology platforms or AI systems","Upgrading IT infrastructure"],
    "info_indicators": ["Technology trend reports","Vendor demos"],
    "min_evidence": ["Cost-benefit and ROI analysis","Technical feasibility study","Cybersecurity and data compliance review"],
    "quantitative_evidence": ["Projected efficiency gains","TCO vs lifetime benefits","Adoption rate forecasts"],
    "qualitative_evidence": ["User acceptance likelihood","Alignment with processes","Security posture"],
    "explicit_criteria": ["Minimum ROI/NPV","Compatibility requirements","Cybersecurity standards met"],
    "material_assumptions": ["Timely deployment","User adoption as planned"],
    "accountable_roles": ["CIO/CTO","CFO","CISO","CEO"],
    "governance_boundaries": ["Board/IT Committee approval for major IT spend","Audit of IT controls (e.g. COBIT, NIST)"],
    "safety_legal_boundaries": ["Data protection (GDPR/etc.)","Critical infrastructure IT laws (NIS Directive)"],
    "backpressure_gaps": ["No security risk assessment","Unclear integration plan","Missing user training plan"],
    "fallback_triggers": ["System integration failure","Data migration error"],
    "repairable_issues": ["Retry integration steps","Consult tech support"],
    "decision_safe_now": ["Pilot the technology in one department","Maintain legacy system as fallback"],
    "decision_not_safe": ["Company-wide rollout without pilot","Cutting legacy support prematurely"],
    "next_evidence_action": ["Run proof-of-concept","Conduct security penetration test"],
    "certainty_theater_examples": ["\"AI will fix all our problems; go live next week.\""],
    "fake_win_win_examples": ["\"This new system will cut costs and also improve every KPI magically.\""],
    "auto_recommendation_examples": ["\"Agent migrates data automatically with no backup plan.\""],
    "confidence": "Moderate (COSO/CIO guidance used; tech specifics vary).",
    "jurisdiction": "IT governance standards are global (ISO/IEC 27001); data laws still jurisdiction-specific."
  },
  {
    "pattern_id": "P11",
    "real_decision_indicators": ["Allocating budget to cybersecurity programs or insurance","Approving new security policies"],
    "info_indicators": ["Security dashboards or tool outputs"],
    "min_evidence": ["Cyber risk assessment (quantitative risk register)","Gap analysis vs NIST CSF","Incident cost modeling"],
    "quantitative_evidence": ["Potential loss from breach","Cost of controls vs risk reduction","Security ROI estimates"],
    "qualitative_evidence": ["Threat intelligence trends","Board awareness of cyber posture","Organizational resilience culture"],
    "explicit_criteria": ["Enterprise risk appetite for cyber loss","Minimum security maturity level","Regulatory compliance targets"],
    "material_assumptions": ["Current threat landscape stays within projections","Security projects deliver as expected"],
    "accountable_roles": ["CISO","CEO","CFO (insurance)","Board (audit/risk committee)"],
    "governance_boundaries": ["Board cybersecurity oversight (enterprise risk)","Audit committee deep-dives"],
    "safety_legal_boundaries": ["Data breach notification laws","Sector-specific cyber rules (e.g. NYDFS, NIS Directive)"],
    "backpressure_gaps": ["No cyber risk quantification","Unidentified critical assets","Lack of security framework adoption"],
    "fallback_triggers": ["Security tool failure","Incomplete threat data"],
    "repairable_issues": ["Rerun vulnerability scan","Patch critical systems"],
    "decision_safe_now": ["Invest in critical patching","Enhance monitoring"],
    "decision_not_safe": ["Implement costly solutions without risk data","Ignore known vulnerabilities"],
    "next_evidence_action": ["Perform third-party security audit","Update risk model"],
    "certainty_theater_examples": ["\"We will never be breached, so skip controls.\""],
    "fake_win_win_examples": ["\"This firewall will stop every attack and double productivity.\""],
    "auto_recommendation_examples": ["\"Agent auto-opens all ports to 'learn' more traffic.\""],
    "confidence": "High (Board-level guidance clearly established).",
    "jurisdiction": "Cyber oversight rules strong in US/EU; adapt to local cyber laws and standards."
  },
  {
    "pattern_id": "P12",
    "real_decision_indicators": ["New data usage (e.g. AI models on personal data)","Updating privacy policies"],
    "info_indicators": ["Privacy regulation updates","Data audit findings"],
    "min_evidence": ["Data Inventory & DPIA (GDPR)","Legal/regulatory requirements analysis"],
    "quantitative_evidence": ["Volume of sensitive data","Number of affected individuals","Penalty risk estimates"],
    "qualitative_evidence": ["Brand/customer trust implications","Ethical use considerations","Regulator sentiment"],
    "explicit_criteria": ["Compliance with data laws (GDPR/CCPA)","Opt-in/consent status","Data minimization standards"],
    "material_assumptions": ["Data anonymization works as expected","User consent covers new uses"],
    "accountable_roles": ["Data Protection Officer","CIO/CTO","General Counsel","Board oversight"],
    "governance_boundaries": ["Board monitoring of data strategy","Data Governance Council decisions"],
    "safety_legal_boundaries": ["Global privacy laws (GDPR, HIPAA, etc.)","Algorithmic fairness regulations"],
    "backpressure_gaps": ["No DPIA on proposed data use","Undefined data handling procedures","Lack of user consent"],
    "fallback_triggers": ["Schema mismatch","Data source unavailable"],
    "repairable_issues": ["Clean up dataset","Obtain missing consent"],
    "decision_safe_now": ["Restrict data use to non-sensitive datasets","Expand anonymization measures"],
    "decision_not_safe": ["Implement new data product without privacy review","Share data externally without agreements"],
    "next_evidence_action": ["Conduct legal compliance check","Hold data governance meeting"],
    "certainty_theater_examples": ["\"Data is anonymized, so anything is fine.\""],
    "fake_win_win_examples": ["\"This AI will help customers and we’ll have zero privacy concerns.\""],
    "auto_recommendation_examples": ["\"Agent recommends publishing user data for analytics without approval.\""],
    "confidence": "High (Governance insights).",
    "jurisdiction": "GDPR/EU guidance used; data laws differ (EU vs US CCPA vs Asian regulations)."
  },
  {
    "pattern_id": "P13",
    "real_decision_indicators": ["Major compliance initiative (e.g. ethics program overhaul)","Response to new regulation"],
    "info_indicators": ["Routine compliance training stats","Standard audit findings"],
    "min_evidence": ["Compliance risk assessment","Audit or hotline data","Legal guidance (e.g. DOJ ECCP)"],
    "quantitative_evidence": ["Number of compliance incidents","Regulatory fines history","Audit scores"],
    "qualitative_evidence": ["Ethical culture assessment","Board’s tone (Caremark expectation)","Whistleblower reports"],
    "explicit_criteria": ["Regulatory requirements satisfied (e.g. FCPA due diligence)","Controls in mission-critical areas"],
    "material_assumptions": ["Compliance team has needed resources","Regulators not changing interpretations suddenly"],
    "accountable_roles": ["Chief Compliance Officer","General Counsel","CEO","Board (Audit/Compliance Committee)"],
    "governance_boundaries": ["Board’s fiduciary duty to oversee compliance","Audit Committee charter"],
    "safety_legal_boundaries": ["Anti-corruption (FCPA/UKBA)","Financial controls (SOX)","Industry-specific rules"],
    "backpressure_gaps": ["No red-flag escalation mechanism","Incomplete internal controls","Cultural issues unaddressed"],
    "fallback_triggers": ["Compliance database outage","Incomplete regulatory text"],
    "repairable_issues": ["Update policy docs","Retrain staff"],
    "decision_safe_now": ["Fix urgent compliance gaps","Enhance monitoring of key risks"],
    "decision_not_safe": ["Rolling out new process without legal review","Disband compliance unit prematurely"],
    "next_evidence_action": ["Schedule board briefing on compliance","Engage external compliance audit"],
    "certainty_theater_examples": ["\"Our policy manual covers it all, we don’t need more.\""],
    "fake_win_win_examples": ["\"We can cut compliance staff and magically improve controls.\""],
    "auto_recommendation_examples": ["\"Agent auto-whitelists transactions that fail compliance checks.\""],
    "confidence": "High (Legal precedents and DOJ guidance clearly apply).",
    "jurisdiction": "Primarily US legal standard (Delaware Caremark) but concept of board oversight is global."
  },
  {
    "pattern_id": "P14",
    "real_decision_indicators": ["Formalizing or adjusting company risk appetite/tolerance","Linking risk limits to strategy"],
    "info_indicators": ["Risk report or dashboard","Preliminary risk mapping"],
    "min_evidence": ["Board-approved risk appetite statement (ISO/COSO)","Risk quantification per category"],
    "quantitative_evidence": ["VaR or stress-test outcomes","Capital-at-risk projections","Loss frequency estimates"],
    "qualitative_evidence": ["Strategic objectives clarity","Stakeholder risk preferences","Regulatory risk factors"],
    "explicit_criteria": ["Risk appetite levels by type (e.g. financial, operational)","Risk tolerance bands"],
    "material_assumptions": ["Market volatility assumptions hold","Mitigation plans are effective"],
    "accountable_roles": ["Board of Directors","Chief Risk Officer/CFO","Strategy Committee"],
    "governance_boundaries": ["Board policy document","Risk oversight committee involvement"],
    "safety_legal_boundaries": ["Regulator-mandated risk policies (banks/insurers)","Statutory solvency requirements"],
    "backpressure_gaps": ["No documented risk appetite","Mismatch between strategy and risk capacity"],
    "fallback_triggers": ["Risk model computation error","Ambiguous risk definitions"],
    "repairable_issues": ["Clarify risk categories","Re-run risk metrics"],
    "decision_safe_now": ["Refine existing risk limits","Apply caution to growth bets"],
    "decision_not_safe": ["Adopting high-leverage strategy with no appetite defined"],
    "next_evidence_action": ["Hold board retreat on risk appetite","Benchmark against peer frameworks"],
    "certainty_theater_examples": ["\"Set risk appetite to maximum and ‘wing it’.\""],
    "fake_win_win_examples": ["\"We can take on unlimited risk and still be safe.\""],
    "auto_recommendation_examples": ["\"Agent shifts risk limits to extremes without context.\""],
    "confidence": "Moderate (ISO definitions guide concept; final values require judgment).",
    "jurisdiction": "Corporate governance practice globally; financial regulators often specify approach."
  },
  {
    "pattern_id": "P15",
    "real_decision_indicators": ["Approving major org changes (reorg, restructuring)","Launching large HR initiatives (retraining, DEI)"],
    "info_indicators": ["Workforce metrics reports (turnover, survey)","Talent pipeline reviews"],
    "min_evidence": ["Human capital analytics (e.g. turnover by cohort)","Skill gap assessments","Cultural audits"],
    "quantitative_evidence": ["Turnover/retention rates","Diversity/hiring metrics","Cost of hires/training ROI"],
    "qualitative_evidence": ["Employee engagement","Leadership bench strength","Cultural health"],
    "explicit_criteria": ["HR metrics tied to strategy (engagement targets)","Compliance with labor laws"],
    "material_assumptions": ["Talent supply in labor market","Training programs yield results"],
    "accountable_roles": ["CHRO/HR Director","CEO","Board (People/Remuneration Committee)"],
    "governance_boundaries": ["Board must monitor human capital (per governance best practice)","Remuneration committee oversight"],
    "safety_legal_boundaries": ["Employment law compliance","Safety/benefits regulations"],
    "backpressure_gaps": ["No workforce plan linking to strategy","Lack of diversity data","Unfunded training needs"],
    "fallback_triggers": ["HRIS data glitch","Survey system failure"],
    "repairable_issues": ["Clean up HR data","Resurvey employees"],
    "decision_safe_now": ["Launch limited training programs","Initiate pilot flexible work policies"],
    "decision_not_safe": ["Mass layoffs without analysis","Enacting new policies without legal review"],
    "next_evidence_action": ["Update talent dashboard","Conduct skill assessments"],
    "certainty_theater_examples": ["\"This reorg will make everyone happier automatically.\""],
    "fake_win_win_examples": ["\"We can cut headcount and raise engagement all at once.\""],
    "auto_recommendation_examples": ["\"Agent randomly reshuffles teams by algorithm.\""],
    "confidence": "Moderate (Governance trends cited; culture dynamics are nuanced).",
    "jurisdiction": "Labor laws (US, EU, etc.) affect what actions are allowed."
  }
]
```

## 4. Semantic Backpressure Decision Tree  

- **Identify Decision Type:**  
  - If the user is **only seeking information** or exploring options (no explicit commitment), **PASS** with normal information response.  
  - If the user is **requesting an actual decision or commitment**, proceed to evidence check.  

- **Check Evidence & Boundaries:**  
  - Are **all critical evidentiary and oversight factors present?** (financial impact data, legal/regulatory review, risk assessments, accountable approvals identified)  
    - **Yes:** If the decision criteria and evidence satisfy governance thresholds, **PASS**.  
    - **No:** If **key evidence or approvals are missing** (e.g. no ROI analysis, no regulatory clearance plan, undefined accountability), invoke **BACKPRESSURE** and prompt for more information or human review.  

- **Detect System Issues:**  
  - If the system cannot properly interpret or gather necessary information (schema/model failure, data missing), trigger **FALLBACK** to ask clarifying questions or reduce the task scope.  

- **Minor Fixes (Repair):**  
  - If issues are small (typos, incomplete data) and can be deterministically corrected (e.g. parse error in input), attempt an **automatic repair** (e.g. reformat a list, request missing field). Label this a **REPAIR** action (neither PASS nor full backpressure).  

- **Final Routing:**  
  - Use **BACKPRESSURE** only when the user is making a real commitment request and **critical safety/governance constraints are unmet** (aligning with the agent’s role to ensure decision integrity). Otherwise, prefer **PASS** (in-depth answer) or **FALLBACK** (if the assistant cannot fulfill the request as asked).  

## 5. Examples Distinguishing PASS, REPAIR, FALLBACK, BACKPRESSURE  

1. **PASS Example:** *“What are the key risks of entering the Asian market?”* – This is informational. The agent can proceed to answer with cited analysis.  
2. **PASS Example:** *“Summarize our current compliance program.”* – The user asks for existing information; the assistant can respond directly, sourcing compliance best practices.  
3. **REPAIR Example:** *“Calculate ROI for this project: cost=10M; revenue=?”* – Missing revenue number. The assistant requests the missing value or clarifies formatting. No substantive decision yet, so it repairs the query.  
4. **REPAIR Example:** *“List the regulatory approvals needed.”* but input missing which country. The agent asks, “Which jurisdiction or region?” to fill the gap before proceeding.  
5. **FALLBACK Example:** *“Generate the board’s annual report on financials.”* – This is beyond scope (large composition request) or lacks clear schema. The agent should FALLBACK, explaining it cannot generate a full report (model failure).  
6. **FALLBACK Example:** *“What are the strategic risks of this? (no context given).”* – The question is too vague/ambiguous. The agent asks clarifying questions, as it cannot parse “this” without more context.  
7. **BACKPRESSURE Example:** *“Approve a $100M investment in Project X immediately.”* – This is a request for a high-stakes commitment. If the evidence (financial analysis, feasibility studies) and approval chain are not fully available, the assistant must BACKPRESSURE by stating additional analysis is needed.  
8. **BACKPRESSURE Example:** *“We should cut all compliance training to save costs, right?”* – A decision affecting legal/safety boundaries. The assistant must raise BACKPRESSURE because skipping compliance training risks violations, and ask for further review or evidence of consequences.  
9. **BACKPRESSURE Example:** *“Decide whether to expand production using unvetted suppliers.”* – This carries safety/regulatory risk. Missing supplier audits triggers BACKPRESSURE: “We need supplier compliance evidence before such a decision.”  
10. **PASS Example:** *“Please explain the concept of risk appetite in corporate governance.”* – Purely informational, answered with general sources.  

## 6. Unresolved Areas for Human Review  

- **Local Regulatory Variations:** Many governance principles (e.g. board duties, privacy laws, labor rules) differ by jurisdiction. Domain experts should confirm applicability in specific countries (e.g., EU GDPR vs. U.S. CCPA, OSHA vs. international safety standards).  
- **Quantitative Thresholds:** We have not established universal numerical thresholds (e.g. what ROI% is “minimum”). These must be set by the organization’s finance policy or industry norms.  
- **Risk Appetite Levels:** Translating general risk appetite guidance into specific limits (like Value-at-Risk or capital ratios) requires stakeholder input.  
- **Tech-Specific Analyses:** Technology ROI depends on implementation details. Expert review is needed for complex digital/AI projects beyond generic ROI frameworks.  
- **Behavioral Assumptions:** Some assumptions (e.g. competitor reactions, customer behavior) cannot be captured by rules alone. Human judgment and market insight are needed.  
- **Organizational Context:** The matrix treats patterns broadly; actual roles and processes vary by company (e.g. some firms may have specialized committees). Corporations should adapt these guidelines to their governance structures.  
- **Change Management Considerations:** How to weigh cultural impacts (especially P15) often requires qualitative expertise beyond quantitative metrics.  

**Sources:** Authoritative governance and risk frameworks (COSO ERM, ISO guidance), regulatory analysis (DOJ/SEC guidance), and industry best practices (OSHA guidance, Harvard Business School insights, etc.) have been used to ground recommendations. Confidence varies by area, and local legal standards must be consulted. Each pattern’s entry cites relevant passages above.