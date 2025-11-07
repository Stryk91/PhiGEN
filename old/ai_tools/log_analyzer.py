"""
AI-Powered Log Analyzer
Analyzes logs for errors, patterns, and anomalies using local AI models
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Add ai_tools to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from ollama_client import OllamaClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LogAnalyzer:
    """Analyze logs using AI for insights and error detection"""

    def __init__(self, model: str = "granite-code:3b"):
        self.client = OllamaClient(model=model)
        self.system_prompt = """You are a log analysis expert. Analyze logs to:
- Identify errors and critical issues
- Detect patterns and anomalies
- Suggest root causes
- Recommend fixes
Provide clear, prioritized findings."""

    def analyze_file(self, log_file: str, last_n_lines: int = 500) -> Dict:
        """
        Analyze a log file

        Args:
            log_file: Path to log file
            last_n_lines: Number of recent lines to analyze

        Returns:
            Analysis results
        """
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # Get recent logs
            recent_logs = lines[-last_n_lines:] if len(lines) > last_n_lines else lines
            log_content = ''.join(recent_logs)

            # Extract errors and warnings
            errors = self._extract_errors(log_content)
            warnings = self._extract_warnings(log_content)

            prompt = f"""Analyze these logs from {log_file}:

Recent log entries ({len(recent_logs)} lines):
```
{log_content[:2000]}
```

Found {len(errors)} errors and {len(warnings)} warnings.

Provide:
1. Critical Issues (if any)
2. Root Cause Analysis
3. Recommended Actions
4. Severity Level (LOW/MEDIUM/HIGH/CRITICAL)
"""

            response = self.client.generate(prompt, system=self.system_prompt)

            return {
                "file": log_file,
                "analysis": response,
                "errors_found": len(errors),
                "warnings_found": len(warnings),
                "sample_errors": errors[:5],
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }

        except Exception as e:
            logger.error(f"Error analyzing {log_file}: {e}")
            return {
                "file": log_file,
                "status": "error",
                "error": str(e)
            }

    def analyze_docker_logs(self, container_name: str, last_n_lines: int = 200) -> Dict:
        """
        Analyze Docker container logs

        Args:
            container_name: Container name
            last_n_lines: Number of lines to analyze

        Returns:
            Analysis results
        """
        import subprocess

        try:
            result = subprocess.run(
                ["docker", "logs", "--tail", str(last_n_lines), container_name],
                capture_output=True,
                text=True
            )

            logs = result.stdout + result.stderr

            if not logs:
                return {"status": "no_logs", "container": container_name}

            prompt = f"""Analyze Docker container logs for {container_name}:

```
{logs[:2000]}
```

Identify:
1. Errors and exceptions
2. Performance issues
3. Configuration problems
4. Potential security issues
5. Recommended fixes
"""

            response = self.client.generate(prompt, system=self.system_prompt)

            return {
                "container": container_name,
                "analysis": response,
                "status": "success",
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error analyzing Docker logs: {e}")
            return {
                "container": container_name,
                "status": "error",
                "error": str(e)
            }

    def monitor_directory(self, log_dir: str, patterns: List[str] = ["*.log"]) -> List[Dict]:
        """
        Monitor all logs in a directory

        Args:
            log_dir: Directory containing logs
            patterns: File patterns to match

        Returns:
            List of analysis results
        """
        results = []
        path = Path(log_dir)

        for pattern in patterns:
            for log_file in path.glob(pattern):
                logger.info(f"Analyzing: {log_file}")
                analysis = self.analyze_file(str(log_file))
                results.append(analysis)

        return results

    def _extract_errors(self, log_content: str) -> List[str]:
        """Extract error messages from logs"""
        error_patterns = [
            r'ERROR.*',
            r'Exception:.*',
            r'Traceback.*',
            r'FATAL.*',
            r'CRITICAL.*',
            r'failed.*',
            r'error:.*'
        ]

        errors = []
        for pattern in error_patterns:
            matches = re.finditer(pattern, log_content, re.IGNORECASE | re.MULTILINE)
            errors.extend([m.group(0) for m in matches])

        return list(set(errors))  # Remove duplicates

    def _extract_warnings(self, log_content: str) -> List[str]:
        """Extract warning messages from logs"""
        warning_patterns = [
            r'WARNING.*',
            r'WARN.*',
            r'deprecated.*'
        ]

        warnings = []
        for pattern in warning_patterns:
            matches = re.finditer(pattern, log_content, re.IGNORECASE | re.MULTILINE)
            warnings.extend([m.group(0) for m in matches])

        return list(set(warnings))

    def generate_summary_report(self, analyses: List[Dict]) -> str:
        """
        Generate summary report from multiple analyses

        Args:
            analyses: List of analysis results

        Returns:
            Markdown formatted report
        """
        report = [f"# Log Analysis Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"]

        total_errors = sum(a.get('errors_found', 0) for a in analyses if a.get('status') == 'success')
        total_warnings = sum(a.get('warnings_found', 0) for a in analyses if a.get('status') == 'success')

        report.append(f"## Summary\n")
        report.append(f"- Files Analyzed: {len(analyses)}")
        report.append(f"- Total Errors: {total_errors}")
        report.append(f"- Total Warnings: {total_warnings}\n")

        report.append(f"## Detailed Analysis\n")

        for analysis in analyses:
            if analysis.get('status') == 'success':
                report.append(f"### {analysis.get('file', analysis.get('container', 'Unknown'))}\n")
                report.append(f"**Errors:** {analysis.get('errors_found', 0)}")
                report.append(f"**Warnings:** {analysis.get('warnings_found', 0)}\n")
                report.append(analysis.get('analysis', ''))
                report.append("\n---\n")

        return "\n".join(report)


def main():
    """Run log analysis from command line"""
    import argparse

    parser = argparse.ArgumentParser(description="AI Log Analyzer")
    parser.add_argument("--file", help="Analyze single log file")
    parser.add_argument("--dir", help="Analyze all logs in directory")
    parser.add_argument("--docker", help="Analyze Docker container logs")
    parser.add_argument("--output", help="Output file for report")
    parser.add_argument("--lines", type=int, default=500, help="Lines to analyze")

    args = parser.parse_args()

    analyzer = LogAnalyzer()

    if not analyzer.client.is_available():
        print("Error: Ollama service not available")
        print(f"Make sure Ollama is running at {analyzer.client.host}")
        sys.exit(1)

    analyses = []

    if args.file:
        analyses = [analyzer.analyze_file(args.file, args.lines)]
    elif args.dir:
        analyses = analyzer.monitor_directory(args.dir)
    elif args.docker:
        analysis = analyzer.analyze_docker_logs(args.docker, args.lines)
        if analysis.get("status") == "success":
            print(analysis["analysis"])
        return

    if analyses:
        report = analyzer.generate_summary_report(analyses)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)


if __name__ == "__main__":
    main()
