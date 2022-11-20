import re
from const import *

def inbounds(bounds, value):
    lower, upper = bounds
    return float(value) >= lower and float(value) < upper

def bias_tag(bias_score):
    tag = ""
    if inbounds(MOST_EXTREME_LEFT, bias_score): tag = "MOST_EXTREME_LEFT"
    elif inbounds(HYPER_PARTISAN_LEFT, bias_score): tag = "HYPER_PARTISAN_LEFT"
    elif inbounds(SKEWS_LEFT, bias_score): tag = "SKEWS_LEFT"
    elif inbounds(BALANCED_BIAS, bias_score): tag = "BALANCED_BIAS"
    elif inbounds(SKEWS_RIGHT, bias_score): tag = "SKEWS_RIGHT"
    elif inbounds(HYPER_PARTISAN_RIGHT, bias_score): tag = "HYPER_PARTISAN_RIGHT"
    elif inbounds(MOST_EXTREME_RIGHT, bias_score): tag = "MOST_EXTREME_RIGHT"
    else:
        raise ValueError(f"Bias score {bias_score} out of range.")
    return tag

def reliability_tag(reliability_score):
    tag = ""
    if inbounds(ORIGINAL_FACT_REPORTING, reliability_score): tag = "ORIGINAL_FACT_REPORTING"
    elif inbounds(FACT_REPORTING, reliability_score): tag = "FACT_REPORTING"
    elif inbounds(COMPLEX_ANALYSIS, reliability_score): tag = "COMPLEX_ANALYSIS"
    elif inbounds(ANALYSIS, reliability_score): tag = "ANALYSIS"
    elif inbounds(OPINION, reliability_score): tag = "OPINION"
    elif inbounds(MISLEADING, reliability_score): tag = "MISLEADING"
    elif inbounds(INNACURATE, reliability_score): tag = "INNACURATE"
    else:
        raise ValueError(f"Reliability score {reliability_score} out of range.")
    return tag

def generate_bias_dict(adfontes_text):
    bias_dict = {}
    bias_scores = []
    for text in adfontes_text:
        text = text.replace("\n", " ")
        bias_score = re.search(r'Bias: -?(\d+\.+\d)', text).group(1)
        reliability_score = re.search(r'Reliability: -?(\d+\.+\d)', text).group(1)
        print(bias_score, reliability_score)
        bias_scores.append((bias_tag(bias_score), reliability_tag(reliability_score)))
    return bias_scores