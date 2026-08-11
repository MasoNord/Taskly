from jinja2 import Environment


class TemplateRenderer:
    def __init__(self, env: Environment) -> None:
        self._env = env

    def render(self, template_name: str, context: dict) -> str:
        template = self._env.get_template(template_name)

        return template.render(**context)
