# Understanding Video on Demand Streaming: YouTube ABR Analysis

**CS204 - Advanced Computer Networks**
**Fall 2025**

**Student:** Conor Fabian
**Email:** cfabi0@ucr.edu
**University of California, Riverside**

---

## Abstract

[150-200 word summary of project, methods, and key findings]

---

## 1. Introduction

### 1.1 Background

Video-on-demand (VoD) services account for a significant portion of global Internet traffic [citation needed]. These platforms rely on adaptive bitrate (ABR) streaming to deliver smooth playback across varying network conditions.

[Expand on importance of ABR, challenges in measuring it, your approach]

### 1.2 Research Questions

This project investigates the following questions:

1. How quickly does YouTube respond to bandwidth changes?
2. What quality levels are selected under different network conditions?
3. How does buffer management influence quality decisions?
4. How aggressively does YouTube recover quality when bandwidth improves?
5. How consistent is the behavior across multiple trials?

### 1.3 Contributions

This project contributes:
- Reproducible methodology for measuring YouTube ABR despite TLS encryption
- Dataset of YouTube playback under controlled network conditions
- Characterization of YouTube's adaptation behavior
- Open-source tools for similar analyses

---

## 2. Background and Related Work

### 2.1 Adaptive Bitrate Streaming

[Explain how ABR works - manifest files, segments, quality selection]

### 2.2 DASH and HLS Protocols

[Describe the protocols YouTube uses]

### 2.3 ABR Algorithms

[Discuss throughput-based, buffer-based, and hybrid approaches]

[Cite: Stockhammer 2011, Akhshabi et al. 2012, others]

### 2.4 Measurement Challenges

[Explain TLS encryption, DRM, why measurement is difficult]

---

## 3. Methodology

### 3.1 Experimental Setup

**Hardware and Software:**
- MacBook Pro (2021) running macOS 14.x
- Google Chrome version X.X
- Python 3.x for analysis

**Test Video:**
- YouTube video ID: [ID]
- Duration: [X] minutes
- Available qualities: 360p, 480p, 720p, 1080p

### 3.2 Network Shaping

We used macOS's packet filter (pfctl) and dummynet (dnctl) to apply controlled network conditions.

**Network Trace:**

| Phase | Time | Bandwidth | Latency |
|-------|------|-----------|---------|
| 1 | 0-45s | 20 Mbps | 40ms |
| 2 | 45-90s | 1.5 Mbps | 40ms |
| 3 | 90-135s | 20 Mbps | 40ms |

[Explain rationale for this trace]

Configuration commands:
```bash
[Include actual commands]
```

### 3.3 Data Collection

We collected data using Chrome's media-internals interface (chrome://media-internals), which provides real-time playback statistics without requiring packet capture.

**Metrics Collected:**
- Video resolution (width x height pixels)
- Video bitrate (kbps)
- Buffer level (seconds)
- Quality switch events (timestamps)
- Player state (playing/buffering/stalled)

[Describe collection procedure]

### 3.4 Experimental Protocol

We conducted 5 trials:
- Trials 001-002: Baseline (no network shaping)
- Trials 003-005: Full network trace

[Describe step-by-step procedure]

**Controls:**
- Same video for all trials
- Same browser profile (cleared between trials)
- Same time of day to minimize ISP variations
- No background network activity

---

## 4. Results

### 4.1 Baseline Behavior (No Network Shaping)

**Figure 1:** Baseline timeline

[Insert figure]

[Describe baseline behavior - initial quality, steady state, buffer levels]

**Table 1:** Baseline metrics

| Metric | Trial 001 | Trial 002 |
|--------|-----------|-----------|
| Avg Bitrate | X kbps | Y kbps |
| Quality Switches | X | Y |
| Avg Buffer | X s | Y s |

### 4.2 Response to Bandwidth Degradation

**Figure 2:** Quality switches during degradation

[Insert figure]

[Describe what happens when bandwidth drops]

**Switch Timing:**
- First switch occurred at T = X +/- Y seconds (mean +/- std dev)
- Quality dropped from [resolution] to [resolution]
- Buffer drained from [X]s to [Y]s

**Table 2:** Phase 2 metrics

| Metric | Trial 003 | Trial 004 | Trial 005 |
|--------|-----------|-----------|-----------|
| Switch delay | X s | Y s | Z s |
| Final quality | Xp | Yp | Zp |
| Min buffer | X s | Y s | Z s |
| Stalls | X | Y | Z |

### 4.3 Recovery Behavior

**Figure 3:** Quality during recovery

[Insert figure]

[Describe how quality recovers when bandwidth returns]

**Recovery Timing:**
- First quality increase at T = X +/- Y seconds
- Final quality: [resolution]
- Did it return to original quality? [yes/no, discuss]

### 4.4 Consistency Across Trials

**Figure 4:** Bitrate overlay of all trials

[Insert figure]

[Discuss consistency - were results similar? variations?]

**Table 3:** Summary statistics

| Metric | Mean | Std Dev |
|--------|------|---------|
| Avg Bitrate | X | Y |
| Quality Switches | X | Y |
| Avg Buffer | X | Y |

---

## 5. Discussion

### 5.1 ABR Algorithm Characteristics

Our results suggest YouTube's ABR algorithm exhibits [characteristics]:

1. [Characteristic 1 with evidence]
2. [Characteristic 2 with evidence]
3. [Characteristic 3 with evidence]

### 5.2 User Experience Implications

[Discuss what these findings mean for users]

### 5.3 Comparison to Prior Work

[How do results compare to previous studies?]

### 5.4 Limitations

This study has several limitations:

1. **Single video:** Results may vary for different content types
2. **Synthetic trace:** Real network conditions more complex
3. **Manual collection:** Some measurement error possible
4. **Small sample:** Only 5 trials conducted
5. [Other limitations]

---

## 6. Conclusion

### 6.1 Summary

[Summarize key findings]

### 6.2 Contributions

This project provides:
- Reproducible methodology
- Open dataset
- Characterization of YouTube ABR
- Tools for future research

### 6.3 Future Work

Future work could:
- Test multiple videos with different characteristics
- Compare across platforms (Netflix, Twitch, etc.)
- Investigate other network conditions (loss, jitter)
- Conduct subjective user studies
- Analyze impact of different ABR algorithms

---

## References

[1] Stockhammer, T. (2011). "Dynamic adaptive streaming over HTTP - standards and design principles." In Proceedings of ACM MMSys.

[2] Akhshabi, S., et al. (2012). "An experimental evaluation of rate-adaptation algorithms in adaptive streaming over HTTP." In Proceedings of ACM MMSys.

[3] RFC 8216: HTTP Live Streaming. https://datatracker.ietf.org/doc/html/rfc8216

[4] ISO/IEC 23009-1: Dynamic Adaptive Streaming over HTTP (DASH).

[Additional references]

---

## Appendices

### Appendix A: Network Trace Specification

[Complete configuration details]

### Appendix B: Data Collection Protocol

[Detailed step-by-step procedure]

### Appendix C: Repository Structure

[GitHub repository organization]
