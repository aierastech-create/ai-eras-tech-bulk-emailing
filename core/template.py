from jinja2 import Template
from typing import Dict
from infra.logger import logger


class TemplateEngine:
    def __init__(self, template_str: str):
        self.template = Template(template_str)

    def render(self, context: Dict) -> str:
        try:
            rendered = self.template.render(**context)
            return rendered
        except Exception as e:
            logger.error(f"Template rendering failed: {e}")
            raise