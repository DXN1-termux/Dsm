import os

class SVGGenerator:
    """Generates clean SVG visualizations for data."""
    @staticmethod
    def generate_disk_pie(percentage, filename="disk_usage.svg"):
        """Simple SVG representation of disk usage."""
        svg_template = f"""<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <circle cx="100" cy="100" r="80" fill="#e0e0e0" />
  <circle cx="100" cy="100" r="80" fill="#3498db" stroke-dasharray="{percentage * 5.02} 502" transform="rotate(-90 100 100)" />
  <text x="50%" y="50%" text-anchor="middle" font-family="Arial" font-size="20" fill="#333">{percentage}%</text>
</svg>"""
        with open(filename, "w") as f:
            f.write(svg_template)
        return os.path.abspath(filename)
