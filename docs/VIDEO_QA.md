# Corda Demo Video QA Report

## File Details
- **Video Path**: `C:\Builds\Genlayer\Corda\Corda-demo-final.mp4`
- **File Size**: 9,090,605 bytes (8.67 MB)
- **Audio Path**: `C:\Builds\Genlayer\Corda\remotion\public\audio\narration.mp3`
- **Audio Duration**: 82.85s
- **Video Duration**: 82.90s
- **Duration Delta**: 0.05s (Within standard 1-frame boundary at 30fps)
- **Resolution**: 1920x1080 (Full HD 1080p)
- **Video Codec**: h264
- **Audio Codec**: aac

## Visual Beat Synchronization
| Beat ID | Visual Content | Audio Synchronization | Status |
| :--- | :--- | :--- | :--- |
| `BEAT_01` | The Privacy Question | Proportional speech segment 01 | PASS |
| `BEAT_02` | Contradiction Exposed | Proportional speech segment 02 | PASS |
| `BEAT_03` | Corda Console Ingestion | Proportional speech segment 03 | PASS |
| `BEAT_04` | GenLayer Comparative Consensus | Proportional speech segment 04 | PASS |
| `BEAT_05` | Finalized Verdict | Proportional speech segment 05 | PASS |
| `BEAT_06` | Tamper-Evident On-Chain Proof | Proportional speech segment 06 | PASS |
| `BEAT_07` | Closing Anthem | Proportional speech segment 07 | PASS |

## Integrity Checks
- [x] Playable MP4 container
- [x] Audio stream multiplexed into MP4
- [x] Zero black frame gaps between beat transitions
- [x] Studionet Contract (`0x70c2F7491A2CC7f81AC05ca964a059c05feD3e92`) accurately shown
- [x] Case B Mismatch Tx (`0x5452df20d06d17850778e6a254fe9606944f0d8bb0da050faefe2fd33de0a099`) displayed
- [x] Case A Match Tx (`0xeb63270182d1999633cf71922261ff9e28d8411216019fa0f5e33fd7656c018c`) displayed
- [x] QA Sign-off: PASS
