from __future__ import annotations

import base64
from pathlib import Path

import pandas as pd
import streamlit as st

from datter.agent import AnalysisAgent
from datter.export import export_zip
from datter.models import AgentLogEntry, AnalysisReport, ScorerConfig
from datter.project import Project, load_projects, match_upload_to_project
from datter.report import report_to_json, report_to_markdown
from datter.token_cost import DEFAULT_EMBEDDING_COST_PER_M, DEFAULT_TOKEN_COST_PER_M

ROOT = Path(__file__).parent
BRAND_DIR = ROOT / "assets" / "brand"
BRAIN_ICON = BRAND_DIR / "brain-icon.png"
WORDMARK = BRAND_DIR / "wordmark.png"

PIPELINE_STEPS = [
    ("IngestAgent", "Ingest"),
    ("ChunkAgent", "Chunk"),
    ("DedupAgent", "Dedup"),
    ("ScoreAgent", "Score"),
    ("SelectAgent", "Select"),
    ("EvalAgent", "Eval"),
    ("ReportAgent", "Report"),
]

PROOF_DISCLAIMER = (
    "Building demo — offline understanding proxy (TF-IDF retrieval + token overlap). "
    "Production claims use developed eval harness."
)


def _img_data_uri(path: Path) -> str:
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def render_brand_header() -> None:
    brain_uri = _img_data_uri(BRAIN_ICON)
    wordmark_uri = _img_data_uri(WORDMARK)
    st.markdown(
        f"""
        <header class="datter-brand">
            <div class="datter-brand-row">
                <img class="datter-brand-icon" src="{brain_uri}" alt="Datter brain logo" />
                <img class="datter-brand-wordmark" src="{wordmark_uri}" alt="datter.ai" />
            </div>
            <p class="datter-brand-tagline">Pre-embedding corpus audit</p>
            <p class="datter-brand-flow">Upload → scan → compress → report</p>
        </header>
        """,
        unsafe_allow_html=True,
    )


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');
        html, body, [class*="css"] {
            font-size: 15px;
            line-height: 1.55;
            -webkit-font-smoothing: antialiased;
            background-color: #0b0f14;
        }
        .stApp {
            background: radial-gradient(1200px 600px at 10% -10%, #152033 0%, #0b0f14 55%);
            font-family: 'DM Sans', sans-serif;
            color: #c8d0dc;
        }
        header[data-testid="stHeader"],
        .stApp > header {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        div[data-testid="stDecoration"] { display: none; }
        [data-testid="stAppViewContainer"] {
            background-color: #0b0f14;
        }
        [data-testid="stMain"] > div:first-child {
            background: transparent;
            border: none;
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3.5rem;
            max-width: 1320px;
        }
        [data-testid="stHorizontalBlock"] {
            gap: 1.25rem;
            align-items: flex-start;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child {
            padding-right: 0.75rem;
            min-width: 320px;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child {
            padding-left: 0.25rem;
        }
        div[data-testid="stProgress"] {
            margin: 0.5rem 0 1rem;
        }
        div[data-testid="stProgress"] > label {
            margin-top: 0.65rem;
            padding-top: 0.15rem;
            font-size: 0.88rem;
            color: #8b98ab;
        }
        div[data-testid="stProgress"] > label p {
            margin: 0;
            line-height: 1.45;
        }
        h1, h2, h3, h4, p, label { font-family: 'DM Sans', sans-serif !important; }
        .stMarkdown, .stCaption { color: #8b98ab; font-size: 0.93rem; line-height: 1.5; }
        .datter-brand {
            margin-bottom: 1.75rem;
            padding-bottom: 1.25rem;
            border-bottom: 1px solid #1e2838;
        }
        .datter-brand-row {
            display: flex;
            align-items: center;
            gap: 0.85rem;
            flex-wrap: wrap;
        }
        .datter-brand-icon {
            width: 56px;
            height: 56px;
            object-fit: contain;
            flex-shrink: 0;
        }
        .datter-brand-wordmark {
            height: 36px;
            width: auto;
            object-fit: contain;
        }
        .datter-brand-tagline {
            margin: 0.65rem 0 0;
            color: #e8edf5;
            font-size: 1.125rem;
            font-weight: 600;
            letter-spacing: -0.01em;
            line-height: 1.35;
        }
        .datter-brand-flow {
            margin: 0.35rem 0 0;
            color: #8b98ab;
            font-size: 0.9rem;
            letter-spacing: 0.02em;
            line-height: 1.45;
        }
        .ig-panel {
            background: linear-gradient(145deg, #121820 0%, #0f141c 100%);
            border: 1px solid #2a3548;
            border-radius: 12px;
            padding: 1.15rem 1.35rem;
            margin-bottom: 0.85rem;
        }
        .ig-panel h2, .ig-panel h3 {
            margin: 0 0 0.75rem;
            color: #8b98ab;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.11em;
            text-transform: uppercase;
            line-height: 1.3;
        }
        .ig-kicker {
            color: #3dd6c3;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.13em;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
            line-height: 1.3;
        }
        .ig-hero {
            display: flex;
            align-items: baseline;
            gap: 0.85rem;
            flex-wrap: wrap;
            margin-bottom: 0.55rem;
        }
        .ig-hero-val {
            font-size: 2.65rem;
            font-weight: 700;
            color: #3dd6c3;
            font-family: 'IBM Plex Mono', monospace;
            line-height: 1.05;
            letter-spacing: -0.02em;
        }
        .ig-hero-val.green { color: #3dd663; }
        .ig-hero-val.white { color: #e8edf5; }
        .ig-hero-sub {
            color: #6b7789;
            font-size: 0.9rem;
            line-height: 1.5;
            letter-spacing: 0.01em;
        }
        .ig-stat-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.7rem;
            margin-top: 0.85rem;
        }
        .ig-stat {
            background: #0b0f14;
            border: 1px solid #1e2838;
            border-radius: 8px;
            padding: 0.75rem 0.85rem;
        }
        .ig-stat .k {
            font-size: 0.72rem;
            color: #6b7789;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            margin-bottom: 0.25rem;
            line-height: 1.3;
        }
        .ig-stat .v {
            font-size: 1.15rem;
            font-weight: 600;
            color: #e8edf5;
            font-family: 'IBM Plex Mono', monospace;
            line-height: 1.25;
            letter-spacing: -0.01em;
        }
        .ig-stat .v.dim { color: #8b98ab; font-size: 0.98rem; }
        .ig-token-flow {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            flex-wrap: wrap;
            margin: 0.55rem 0;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 1rem;
            line-height: 1.4;
        }
        .ig-token-flow .before { color: #8b98ab; }
        .ig-token-flow .arrow { color: #3dd6c3; font-weight: 700; }
        .ig-token-flow .after { color: #e8edf5; font-weight: 600; }
        .ig-disclaimer {
            color: #6b7789;
            font-size: 0.82rem;
            line-height: 1.5;
            margin-top: 0.55rem;
            font-style: italic;
        }
        .ig-upload-wrap {
            border: 2px dashed #3a465a;
            border-radius: 10px;
            padding: 1.5rem 1.25rem;
            text-align: center;
            background: rgba(18, 24, 32, 0.5);
            margin-bottom: 1rem;
        }
        .ig-upload-wrap .icon { font-size: 1.85rem; margin-bottom: 0.4rem; opacity: 0.7; }
        .ig-upload-wrap .title { color: #e8edf5; font-weight: 600; font-size: 1.02rem; line-height: 1.35; }
        .ig-upload-wrap .sub { color: #6b7789; font-size: 0.88rem; margin-top: 0.25rem; line-height: 1.45; }
        .ig-chip-row { display: flex; gap: 0.45rem; flex-wrap: wrap; margin: 0.55rem 0; }
        .ig-chip {
            background: #0f141c;
            border: 1px solid #1e2838;
            border-radius: 6px;
            padding: 0.38rem 0.7rem;
            color: #5c6878;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }
        .ig-footnote {
            color: #5c6878;
            font-size: 0.84rem;
            line-height: 1.55;
            margin-top: 0.85rem;
        }
        .ig-empty {
            background: #121820;
            border: 1px dashed #2a3548;
            border-radius: 12px;
            padding: 2.75rem 1.5rem;
            text-align: center;
            color: #8b98ab;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        .ig-regime-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.7rem; }
        .ig-regime {
            background: #0b0f14;
            border: 1px solid #1e2838;
            border-radius: 8px;
            padding: 0.85rem;
            text-align: center;
        }
        .ig-regime.highlight { border-color: #3dd6c3; background: rgba(61,214,195,0.05); }
        .ig-regime .pct { font-size: 1.45rem; font-weight: 700; color: #e8edf5; font-family: 'IBM Plex Mono', monospace; line-height: 1.2; }
        .ig-regime .label { font-size: 0.74rem; color: #8b98ab; text-transform: uppercase; letter-spacing: 0.07em; margin-top: 0.25rem; line-height: 1.3; }
        .ig-regime .hint { font-size: 0.78rem; color: #5c6878; margin-top: 0.3rem; line-height: 1.4; }
        .ig-export-panel {
            margin-top: 0.25rem;
            margin-bottom: 0.5rem;
        }
        .ig-export-panel h3 { margin-bottom: 0; }
        .ig-scan-status {
            margin: 0.35rem 0 0.75rem;
            color: #8b98ab;
            font-size: 0.88rem;
            line-height: 1.5;
        }
        .ig-scan-status strong { color: #e8edf5; }
        .datter-warn {
            background: rgba(245,200,66,0.08);
            border: 1px solid rgba(245,200,66,0.35);
            border-radius: 8px;
            padding: 0.7rem 0.9rem;
            color: #f5c842;
            font-size: 0.84rem;
            line-height: 1.5;
            margin-bottom: 0.85rem;
        }
        div[data-testid="stFileUploader"] section {
            padding: 0;
            border: none;
            background: transparent;
        }
        div[data-testid="stFileUploader"] section > div { padding: 0; }
        div[data-testid="stSidebar"] {
            background: #0b0f14;
            border-right: 1px solid #1e2838;
        }
        div[data-testid="stSidebar"] .stButton > button {
            background: #121820;
            border: 1px solid #2a3548;
            color: #c8d0dc;
            font-size: 0.88rem;
            line-height: 1.4;
        }
        div[data-testid="stSidebar"] .stButton > button:hover {
            border-color: #3dd6c3;
            color: #3dd6c3;
        }
        .stDownloadButton > button {
            background: linear-gradient(135deg, #1a3a35 0%, #121820 100%);
            border: 1px solid #3dd6c3;
            color: #3dd6c3;
            font-weight: 600;
            font-size: 0.88rem;
            border-radius: 8px;
            line-height: 1.4;
        }
        .stDownloadButton > button:hover {
            border-color: #3dd663;
            color: #3dd663;
        }
        div[data-testid="stExpander"] {
            background: #0f141c;
            border: 1px solid #1e2838;
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _step_statuses(entries: list[AgentLogEntry]) -> dict[str, str]:
    statuses = {name: "pending" for name, _ in PIPELINE_STEPS}
    for entry in entries:
        if entry.agent not in statuses:
            continue
        if entry.status == "completed":
            statuses[entry.agent] = "done"
        elif entry.status in {"started", "warning"}:
            if statuses[entry.agent] != "done":
                statuses[entry.agent] = "active"
    return statuses


def progress_from_log(entries: list[AgentLogEntry]) -> float:
    statuses = _step_statuses(entries)
    done = sum(1 for s in statuses.values() if s == "done")
    active = sum(1 for s in statuses.values() if s == "active")
    return min(1.0, (done + 0.35 * active) / len(PIPELINE_STEPS))


def latest_log_message(entries: list[AgentLogEntry]) -> str:
    if not entries:
        return "Waiting to start…"
    entry = entries[-1]
    hints = {
        "IngestAgent": "Loading documents…",
        "ChunkAgent": "Token-aware chunking…",
        "DedupAgent": "Finding duplicates…",
        "ScoreAgent": "Measuring information density (model-agnostic)…",
        "SelectAgent": "Optimising token budget…",
        "EvalAgent": "Running proof loop…",
        "ReportAgent": "Building audit report…",
    }
    if entry.status == "completed":
        return entry.message
    return hints.get(entry.agent, entry.message)


def upload_fingerprint(uploads: list) -> tuple:
    return tuple((u.name, u.size) for u in uploads) if uploads else ()


def quality_score(report: AnalysisReport) -> float:
    if report.eval_summary and report.eval_summary.understanding_pct:
        return report.eval_summary.understanding_pct
    if not report.scores.empty and "usefulness_score" in report.scores.columns:
        return float(report.scores["usefulness_score"].mean() * 100)
    return max(0.0, min(100.0, 100.0 - report.pct_removable))


def token_before_after(report: AnalysisReport) -> tuple[int, int]:
    before = report.selection.full_tokens if report.selection else report.total_tokens
    after = report.optimised_corpus_tokens or (before - report.avoidable_tokens)
    return before, after


def compute_regime_pct(report: AnalysisReport) -> tuple[float, float, float]:
    if report.scores.empty or report.total_tokens == 0:
        return 0.0, 0.0, 0.0
    keep_t = edge_t = ghost_t = 0
    for _, row in report.scores.iterrows():
        tokens = int(row.get("token_count", 0))
        action = row.get("recommended_action", "review")
        if action == "keep":
            keep_t += tokens
        elif action == "drop":
            ghost_t += tokens
        else:
            edge_t += tokens
    total = report.total_tokens
    return keep_t / total * 100, edge_t / total * 100, ghost_t / total * 100


def compression_pct(report: AnalysisReport) -> float:
    if report.selection and report.selection.full_tokens:
        saved = report.selection.full_tokens - report.optimised_corpus_tokens
        return saved / report.selection.full_tokens * 100
    return report.pct_removable


def render_compression_panel(report: AnalysisReport, compressed: float) -> None:
    before, after = token_before_after(report)
    st.markdown(
        f"""
        <div class="ig-panel">
            <h3>A · Compression</h3>
            <div class="ig-hero">
                <span class="ig-hero-val">{compressed:.1f}%</span>
                <span class="ig-hero-sub">max safe cut in optimised export</span>
            </div>
            <div class="ig-token-flow">
                <span class="before">{before:,}</span>
                <span class="arrow">→</span>
                <span class="after">{after:,} tokens</span>
            </div>
            <div class="ig-stat-row">
                <div class="ig-stat">
                    <div class="k">Avoidable</div>
                    <div class="v">{report.avoidable_tokens:,}</div>
                </div>
                <div class="ig-stat">
                    <div class="k">Redundant %</div>
                    <div class="v">{report.pct_removable:.1f}%</div>
                </div>
                <div class="ig-stat">
                    <div class="k">Corpus size</div>
                    <div class="v dim">{report.total_tokens:,} total</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quality_panel(report: AnalysisReport) -> None:
    has_eval = bool(report.eval_summary and report.eval_summary.understanding_pct)
    if has_eval:
        pct = report.eval_summary.understanding_pct
        hero_class = "green" if pct >= 70 else "white"
        sub = "understanding retained at this cut (eval harness)"
        disclaimer = ""
    else:
        pct = quality_score(report)
        hero_class = "white"
        sub = "mean chunk usefulness — not Q&A understanding"
        disclaimer = (
            '<p class="ig-disclaimer">No eval queries attached. Use <b>Try sample</b> '
            "in the sidebar, upload a known demo PDF, or add queries.json for proof-loop metrics.</p>"
        )
    st.markdown(
        f"""
        <div class="ig-panel">
            <h3>B · Quality retained</h3>
            <div class="ig-hero">
                <span class="ig-hero-val {hero_class}">{pct:.1f}%</span>
                <span class="ig-hero-sub">{sub}</span>
            </div>
            {disclaimer}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_savings_panel(report: AnalysisReport, compressed: float) -> None:
    st.markdown(
        f"""
        <div class="ig-panel">
            <h3>C · ROI / savings</h3>
            <div class="ig-hero">
                <span class="ig-hero-val green">${report.avoidable_cost_usd:,.2f}</span>
                <span class="ig-hero-sub">avoidable embedding spend identified</span>
            </div>
            <div class="ig-stat-row">
                <div class="ig-stat">
                    <div class="k">Token cut</div>
                    <div class="v">{compressed:.1f}%</div>
                </div>
                <div class="ig-stat">
                    <div class="k">Full corpus cost</div>
                    <div class="v dim">${report.total_cost_usd:,.2f}</div>
                </div>
                <div class="ig-stat">
                    <div class="k">After optimisation</div>
                    <div class="v dim">${report.total_cost_usd - report.avoidable_cost_usd:,.2f}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_regime_cards(core: float, edge: float, ghost: float) -> None:
    st.markdown(
        f"""
        <div class="ig-regime-row">
            <div class="ig-regime highlight">
                <div class="pct">{core:.0f}%</div>
                <div class="label">Core-Set</div>
                <div class="hint">High-value keep chunks</div>
            </div>
            <div class="ig-regime">
                <div class="pct">{edge:.0f}%</div>
                <div class="label">Edge Cases</div>
                <div class="hint">Review / compress</div>
            </div>
            <div class="ig-regime">
                <div class="pct">{ghost:.0f}%</div>
                <div class="label">Ghost Data</div>
                <div class="hint">Drop / zero value</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_download_ctas(report: AnalysisReport) -> None:
    zip_bytes = b""
    if report.selection and report.chunks:
        zip_bytes = export_zip(report.chunks, report.scores, report.selection)

    st.markdown(
        """
        <div class="ig-panel ig-export-panel">
            <h3>Export & next steps</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        if zip_bytes:
            st.download_button(
                "Download optimised corpus (.zip)",
                zip_bytes,
                file_name=f"datter_{report.project_id or 'upload'}_optimised.zip",
                use_container_width=True,
            )
        else:
            st.caption("Optimised corpus unavailable — re-run scan.")
    with c2:
        st.download_button(
            "Download audit report (.md)",
            report_to_markdown(report),
            file_name="datter_report.md",
            use_container_width=True,
        )


def render_results_panels(report: AnalysisReport) -> None:
    core, edge, ghost = compute_regime_pct(report)
    compressed = compression_pct(report)

    render_compression_panel(report, compressed)
    render_quality_panel(report)
    render_savings_panel(report, compressed)
    render_download_ctas(report)

    with st.expander("Report preview (Markdown)", expanded=False):
        st.markdown(report_to_markdown(report))

    render_advanced_expander(report, core, edge, ghost)


def render_advanced_expander(
    report: AnalysisReport,
    core: float,
    edge: float,
    ghost: float,
) -> None:
    with st.expander("Advanced audit & proof", expanded=False):
        st.markdown('<h4 style="color:#8b98ab;font-size:0.78rem;letter-spacing:0.11em;text-transform:uppercase;line-height:1.3;">Regime labeling</h4>', unsafe_allow_html=True)
        render_regime_cards(core, edge, ghost)
        st.download_button(
            "Download audit log (.json)",
            report_to_json(report),
            file_name="datter_report.json",
            use_container_width=True,
        )

        ev = report.eval_summary
        if ev:
            st.markdown(f'<div class="datter-warn">{PROOF_DISCLAIMER}</div>', unsafe_allow_html=True)
            if ev.questions:
                rows = []
                for q in ev.questions:
                    rows.append({
                        "Question": q.query,
                        "Datter score": q.datter_score,
                        "Random score": q.random_score,
                        "Missing": q.missing_points,
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            if ev.pareto_points:
                pareto_df = pd.DataFrame(
                    {
                        "label": [p.label for p in ev.pareto_points],
                        "understanding": [p.understanding_pct for p in ev.pareto_points],
                        "reduction": [p.token_reduction_pct for p in ev.pareto_points],
                    }
                )
                st.scatter_chart(pareto_df, x="reduction", y="understanding", color="label", size=80)

        display_cols = [
            "item_id", "filename", "token_count", "usefulness_score",
            "recommended_action", "text_preview",
        ]
        with st.expander("Top useful chunks", expanded=False):
            cols = [c for c in display_cols if c in report.top_useful.columns]
            st.dataframe(report.top_useful[cols], use_container_width=True, hide_index=True)
        with st.expander("Most redundant chunks", expanded=False):
            cols = [c for c in display_cols if c in report.most_redundant.columns]
            st.dataframe(report.most_redundant[cols], use_container_width=True, hide_index=True)


def run_streaming(
    agent: AnalysisAgent,
    stream,
    progress_bar,
    status_slot,
) -> AnalysisReport | None:
    report: AnalysisReport | None = None
    for event in stream:
        if isinstance(event, list):
            progress_bar.progress(progress_from_log(event), text="Structural Scan")
            status_slot.markdown(
                f'<p class="ig-scan-status"><strong>Processing…</strong><br>'
                f"{latest_log_message(event)}</p>",
                unsafe_allow_html=True,
            )
        elif isinstance(event, AnalysisReport):
            report = event
            progress_bar.progress(1.0, text="Complete")
            status_slot.markdown(
                '<p class="ig-scan-status"><strong>Complete</strong> — audit ready.</p>',
                unsafe_allow_html=True,
            )
    return report


def build_agent(
    scorer_mode: str,
    token_cost: float,
    embed_cost: float,
    project: Project | None = None,
    uploads: list | None = None,
) -> AnalysisAgent:
    config = ScorerConfig()
    if project is None and uploads:
        project = match_upload_to_project(uploads, ROOT)

    if project:
        return AnalysisAgent(
            scorer_mode=scorer_mode,
            scorer_config=config,
            token_cost_per_m=token_cost,
            embedding_cost_per_m=embed_cost,
            project_id=project.id,
            project_name=project.name,
            queries_path=project.queries_path if project.queries_path.is_file() else None,
            target_token_reduction=project.target_token_reduction,
            eval_cache_path=project.corpus_path / "eval_cache.json",
        )
    return AnalysisAgent(
        scorer_mode=scorer_mode,
        scorer_config=config,
        token_cost_per_m=token_cost,
        embedding_cost_per_m=embed_cost,
        project_id="upload",
        project_name="Uploaded corpus",
        queries_path=None,
        target_token_reduction=0.50,
        eval_cache_path=None,
    )


def render_input_gate_left(scanning: bool) -> list:
    st.markdown(
        """
        <div class="ig-kicker">The input gate</div>
        <div class="ig-upload-wrap">
            <div class="icon">☁</div>
            <div class="title">Upload dataset</div>
            <div class="sub">Drag & drop or browse files below</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    uploaded = st.file_uploader(
        "Corpus files",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="corpus_uploader",
    )
    uploads = uploaded or []

    st.markdown(
        """
        <div class="ig-chip-row">
            <span class="ig-chip">S3 · coming soon</span>
            <span class="ig-chip">SQL · coming soon</span>
            <span class="ig-chip">Kafka · coming soon</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if scanning:
        st.markdown("#### Structural Scan")
    elif uploads:
        matched = match_upload_to_project(uploads, ROOT)
        if matched:
            st.success(
                f"{len(uploads)} file(s) ready — matched **{matched.name}**; proof loop runs on scan."
            )
        else:
            st.success(f"{len(uploads)} file(s) ready — scan runs automatically.")
    else:
        st.info("Upload PDF, TXT, or MD files to begin.")

    st.markdown(
        """
        <p class="ig-footnote">
        We measure raw signal density first — whether you're training an LLM,
        building RAG, or auditing documents. Datter finds the max cut before embedding spend.
        </p>
        """,
        unsafe_allow_html=True,
    )
    return uploads


def render_empty_results() -> None:
    st.markdown(
        """
        <div class="ig-empty">
            <div style="font-size:2.15rem;margin-bottom:0.55rem;">📊</div>
            <div style="font-size:1.15rem;color:#e8edf5;font-weight:600;margin-bottom:0.4rem;line-height:1.35;">
                Upload a corpus to start
            </div>
            <div>Or pick <b>Try sample → Lab</b> in the sidebar for a fast demo.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(
    page_title="Datter.ai",
    page_icon=str(BRAIN_ICON),
    layout="wide",
    initial_sidebar_state="expanded",
)

for key, default in [
    ("cached_report", None),
    ("run_requested", False),
    ("run_mode", None),
    ("sample_project_id", None),
    ("upload_fingerprint", None),
    ("scanning", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

projects = load_projects(ROOT)
projects_by_id = {p.id: p for p in projects}

inject_styles()
render_brand_header()

if "scorer_mode" not in st.session_state:
    st.session_state.scorer_mode = "baseline"
if "token_cost" not in st.session_state:
    st.session_state.token_cost = DEFAULT_TOKEN_COST_PER_M
if "embed_cost" not in st.session_state:
    st.session_state.embed_cost = DEFAULT_EMBEDDING_COST_PER_M

with st.sidebar:
    st.markdown("### Try sample")
    st.caption("Pre-built corpora with eval questions.")
    for project in projects:
        if st.button(
            f"{project.domain} — {project.primary_pdf or 'mixed'}",
            key=f"sample_{project.id}",
            use_container_width=True,
        ):
            st.session_state.run_mode = "sample"
            st.session_state.sample_project_id = project.id
            st.session_state.run_requested = True
            st.session_state.scanning = True

    with st.expander("Advanced", expanded=False):
        st.session_state.scorer_mode = st.radio(
            "Scorer", ["baseline", "adisorn", "hybrid"], index=0, key="scorer_radio"
        )
        st.session_state.token_cost = st.number_input(
            "Token $/1M", value=st.session_state.token_cost, format="%.4f", key="token_cost_input"
        )
        st.session_state.embed_cost = st.number_input(
            "Embed $/1M", value=st.session_state.embed_cost, format="%.4f", key="embed_cost_input"
        )

    if st.button("Re-scan", use_container_width=True):
        if st.session_state.run_mode or st.session_state.cached_report:
            st.session_state.run_requested = True
            st.session_state.scanning = True
        else:
            st.warning("Upload files or load a sample first.")

left_col, right_col = st.columns([2, 3], gap="large")

with left_col:
    progress_bar = st.empty()
    status_slot = st.empty()
    uploads = render_input_gate_left(st.session_state.scanning)
    if uploads:
        fp = upload_fingerprint(uploads)
        if fp != st.session_state.upload_fingerprint:
            st.session_state.upload_fingerprint = fp
            st.session_state.run_mode = "upload"
            st.session_state.run_requested = True
            st.session_state.scanning = True
            st.session_state.sample_project_id = None

report: AnalysisReport | None = None
should_run = st.session_state.run_requested

if should_run:
    agent_kwargs = {
        "scorer_mode": st.session_state.scorer_mode,
        "token_cost": st.session_state.token_cost,
        "embed_cost": st.session_state.embed_cost,
    }
    try:
        if st.session_state.run_mode == "sample" and st.session_state.sample_project_id:
            project = projects_by_id.get(st.session_state.sample_project_id)
            if not project:
                st.error("Sample project not found.")
            else:
                agent = build_agent(project=project, **agent_kwargs)
                stream = agent.stream_from_folder(str(project.corpus_path))
                report = run_streaming(agent, stream, progress_bar, status_slot)
        elif st.session_state.run_mode == "upload" and uploads:
            agent = build_agent(project=None, uploads=uploads, **agent_kwargs)
            stream = agent.stream_from_uploads(uploads)
            report = run_streaming(agent, stream, progress_bar, status_slot)
        else:
            st.session_state.run_requested = False
            st.session_state.scanning = False
    except Exception as exc:
        st.error(f"Analysis failed: {exc}")
        st.session_state.scanning = False
        st.session_state.run_requested = False
    else:
        st.session_state.run_requested = False
        st.session_state.scanning = False
        if report:
            st.session_state.cached_report = report

display = report or st.session_state.cached_report

with right_col:
    if display:
        render_results_panels(display)
    else:
        render_empty_results()
