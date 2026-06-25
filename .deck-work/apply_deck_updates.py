#!/usr/bin/env python3
"""Apply pitch deck alignment text updates to unpacked PPTX XML."""
from __future__ import annotations

import re
from pathlib import Path

UNPACKED = Path(__file__).parent / "unpacked"
SLIDES = UNPACKED / "ppt" / "slides"

# Global replacements: (old, new) applied to all slide files when old found
GLOBAL_REPLACEMENTS: list[tuple[str, str]] = []

# Per-file replacements
FILE_REPLACEMENTS: dict[str, list[tuple[str, str]]] = {
    "slide1.xml": [
        ("TheSis To Thing 3mT", "Selection engine · max cut @ quality floor"),
        (" Live", " · Hands Off London 2026"),
    ],
    "slide2.xml": [
        (
            'Globally, $26B is wasted annually on "Dark Data" storage, and billions more on unproductive GPU compute.',
            'Globally, $26B is wasted annually on "Dark Data" storage, and billions more on unproductive GPU compute. '
            'Move from "Is the data clean?" to "Is this data worth AI spend?"',
        ),
    ],
    "slide5.xml": [
        ("What Data Actually Good", "Where Useful Data Lives"),
        ("HIGH USEFULNESS", "Regime labels support audit — SKU is max safe cut @ eval floor"),
    ],
    "slide6.xml": [
        ("A. Complexity Score", "A. Max Safe Cut @ 90% Floor"),
        ("<a:t>72</a:t>", "<a:t>50%</a:t>"),
        ("Low Score (Redundant)", "90.1% understanding retained"),
        ("Optimal Zone (Informative)", "Building demo — offline eval proxy"),
        ("High Score (Chaotic)", "Gov PDF proof · Treasury handbook"),
        ("Analysis of 10TB complete. 4.2TB identified as redundant.", "Treasury PDF complete. 50% max safe cut @ 90% floor."),
        ("Labeling Savings", "Token Savings"),
        ("$12,500", "65k tokens removed"),
        ("GPU Savings", "Embedding Savings"),
        ("$45,000", "$840 projected"),
        ('Is the data learnable?', "Is this data worth AI spend?"),
    ],
    "slide7.xml": [
        ("Market Opportunity: Riding the AI Data Wave", "Market Opportunity: Pre-Embedding RAG Waste"),
        (
            "Entering at the inflection point: AI teams are drowning in data waste",
            "Every RAG team embeds full PDF libraries before knowing what their bot needs",
        ),
        (" Doubled in 2026", " Pre-embed spend at risk"),
        ("$46.8 Billion", "~$45B+"),
        (
            "Global AI Data Management &amp; Preparation.",
            "Global AI data ingestion, embedding &amp; prep spend.",
        ),
        ("Explosive growth driven by Generative AI.", "Before downstream training &amp; labeling compounds."),
        ("+70% YoY", "RAG wedge"),
        ("$8.5 Billion", "~$8B"),
        (
            "AI-Ready Data Curation &amp; ML Observability.",
            "Pre-embedding corpus optimisation for RAG + fine-tuning teams.",
        ),
        (
            "Teams actively buying clean data tools.",
            "Proactive input gate — not post-hoc observability.",
        ),
        (
            "Early Adopters in Data-Heavy Verticals.",
            "Year 1–3 wedge: RAG teams, regulated KB, ML labs.",
        ),
        (" AV", " RAG Teams"),
        (" IoT", " Regulated KB"),
        (" LLM Labs", " ML Labs"),
    ],
    "slide11.xml": [
        (
            "Simple REST API for raw datasets. Upload batches directly or connect via S3/GCP buckets for continuous evaluation.",
            "Upload PDF corpora + eval questions. Run hands-off audit before embedding into your vector store.",
        ),
        (
            "Receive a per-sample usefulness score and regime label (Order, Complexity, Chaos) to filter your data automatically.",
            "Receive optimised corpus zip, audit manifest, and max safe cut @ floor report — eval-proven vs random.",
        ),
        ("30–50", "Up to 50"),
        ("Reduction in labelling &amp; training waste", "max safe token cut @ 90% floor (Gov demo)"),
        ("# Analyze dataset batch", "# Audit PDF corpus before embed"),
        ('"s3://raw-images/batch-04"', '"gov_handbook.pdf"'),
        (' modality', " corpus"),
        ('="image"', '="Managing Public Money.pdf"'),
        ('"image"', '"Managing Public Money.pdf"'),
        ("Avg. Complexity:", "Max Safe Cut:"),
        ("<a:t>0.72</a:t>", "<a:t>50%</a:t>"),
        ("Recommended Action:", "Understanding @ Cut:"),
        ("Keep 64% (High Signal)", "90.1% (offline proxy)"),
        ("Total Samples:", "Corpus Tokens:"),
        ("50,000", "131k"),
    ],
    "slide12.xml": [
        ("Value-Driven Pricing: ROI-First Model", "Quality-Floor Pricing — You Pick the Floor, We Find the Max Cut"),
        ("Usage Based", "Standard"),
        ("Ideal for POCs &amp; Research", "90% understanding floor"),
        ("$1–$5", "Designed for"),
        ("per GB (or prepaid credits)", "RAG teams &amp; support bots"),
        ("Pay-as-you-go API", "$/M tokens analysed"),
        ("Universal Complexity Metric", "Max safe cut @ floor report"),
        ("Public cloud support", "Eval proof vs random cut"),
        ("Instant ROI Reporting", "Free Audit wedge (local PLG)"),
        ("Team Licence", "Assured"),
        ("Capped &amp; Predictable", "95% understanding floor"),
        ("$10k–50k", "Regulated"),
        ("per year / per team", "internal KB buyers"),
        ("Unlimited analysis (capped)", "$/project/month"),
        ("Shared Team Dashboard", "Audit manifest + export"),
        ("Drift &amp; Junk Detection Alerts", "Quality-floor SLA headroom"),
        ("Pipeline Integration (Airflow)", "Pipeline integration (Airflow)"),
        ("Enterprise ", "Governed "),
        ("Security &amp; Scale", "99% understanding floor"),
        ("Custom Model Weights &amp; Deployment", "On-premise deployment"),
        ("Enterprise + VPC Model Weights &amp; Deployment", "On-premise deployment"),
        ("Custom", "Enterprise + VPC"),
        ("On-premise air-gap", "Immutable audit trail"),
        ("Dedicated Data Opt. Architect", "Dedicated solution architect"),
        ("SLA Guarantees", "SLA guarantees"),
        (
            "Typical customer saves ",
            "Typical customer saves ",
        ),
        (
            "3–5x the subscription cost",
            "3–5x downstream waste",
        ),
        (
            " in reduced labeling/compute fees",
            " vs subscription at same quality floor",
        ),
        ("decisions saved", "max safe cut @ your floor"),
        (", not labels produced.", ", not blind deletion."),
    ],
    "slide13.xml": [
        ("Secure 5-10 ", "5 design-partner "),
        ("Tier 1 AI Lab Partners", "RAG pilots → 5 paying teams"),
        (
            "Focus on high-value design partnerships to validate the data usefulness engine.",
            "Standard tier ($/M analysed) on scoped corpora. Pilot → paid conversion.",
        ),
        ("$0 - $500k", "$0–$500k"),
    ],
}

SLIDE4_TEXT_BOXES = """
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="136" name="Bridge Title"/>
          <p:cNvSpPr txBox="1"/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="761695" y="800000"/>
            <a:ext cx="10600000" cy="900000"/>
          </a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:noFill/><a:ln><a:noFill/></a:ln>
        </p:spPr>
        <p:txBody>
          <a:bodyPr anchorCtr="0" anchor="t" wrap="square"><a:spAutoFit/></a:bodyPr>
          <a:lstStyle/>
          <a:p>
            <a:pPr algn="l"><a:buNone/></a:pPr>
            <a:r>
              <a:rPr b="1" sz="3600" lang="en-US">
                <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
                <a:latin typeface="Space Grotesk"/>
              </a:rPr>
              <a:t>The Input Gate — Before Spend Compounds</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="137" name="Bridge Body"/>
          <p:cNvSpPr txBox="1"/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="761695" y="1900000"/>
            <a:ext cx="10600000" cy="3200000"/>
          </a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:noFill/><a:ln><a:noFill/></a:ln>
        </p:spPr>
        <p:txBody>
          <a:bodyPr anchorCtr="0" anchor="t" wrap="square"><a:spAutoFit/></a:bodyPr>
          <a:lstStyle/>
          <a:p>
            <a:pPr algn="l"><a:buNone/></a:pPr>
            <a:r>
              <a:rPr sz="1800" lang="en-US">
                <a:solidFill><a:srgbClr val="CCCCCC"/></a:solidFill>
                <a:latin typeface="Inter"/>
              </a:rPr>
              <a:t>Datter is a selection engine. You pick a quality floor (90/95/99%). We find the maximum token cut that preserves it — eval-proven vs random at the same budget.</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>
"""


def apply_replacements(content: str, replacements: list[tuple[str, str]]) -> str:
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
    return content


def patch_slide4() -> None:
    path = SLIDES / "slide4.xml"
    content = path.read_text(encoding="utf-8")
    if "The Input Gate — Before Spend Compounds" in content:
        return
    marker = "      <p:pic>"
    if marker not in content:
        raise RuntimeError("slide4.xml: could not find pic marker")
    content = content.replace(marker, SLIDE4_TEXT_BOXES + "\n" + marker, 1)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    for slide_path in sorted(SLIDES.glob("slide*.xml")):
        name = slide_path.name
        content = slide_path.read_text(encoding="utf-8")
        reps = list(GLOBAL_REPLACEMENTS)
        reps.extend(FILE_REPLACEMENTS.get(name, []))
        new_content = apply_replacements(content, reps)
        if new_content != content:
            slide_path.write_text(new_content, encoding="utf-8")
            print(f"updated {name}")
    patch_slide4()
    print("slide4 bridge content added")


if __name__ == "__main__":
    main()
