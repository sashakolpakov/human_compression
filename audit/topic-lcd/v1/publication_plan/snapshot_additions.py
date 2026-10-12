# Proposed additions only. Root integrates these functions and main dispatch;
# every one of the 121 old non-main function ASTs must remain unchanged.
def check_lcd_publication():
    from check_lcd_publication import verify
    return verify(ROOT)

def check_programme50():
    from check_programme50 import verify
    report, _ = verify(ROOT)
    return report

def check_overview50():
    import json, subprocess, sys, tempfile
    from pathlib import Path
    folder = ROOT / 'audit/overview/v16/packet'
    with tempfile.TemporaryDirectory(prefix='overview50-root-') as work:
        output = Path(work) / 'replay'
        subprocess.run([sys.executable, '-B', '-O', str(folder/'check.py'),
                        '--out', str(output)], check=True, capture_output=True, text=True)
        report = json.loads((output/'report.json').read_text())
    if report['exact_fractions'] != 69 or report['SVG_bars'] != 157:
        raise ValueError('Incomplete overview50 replay')
    current = json.loads((ROOT/'audit/corpus/latest.json').read_text())
    results = json.loads((folder/'results.json').read_text())
    if (set(results['original_ids']) != set(current['admitted_original_ids'])
            or current['admitted_principal_originals'] != 50
            or current['accessible_pending_complete_recovery'] != 56):
        raise ValueError('Overview and actual public programme differ')
    return 69, 157
