import os
import hashlib

from jinja2.sandbox import SandboxedEnvironment


def hash_md5(data: bytes) -> str:
    enc = hashlib.md5()
    enc.update(data)
    return enc.hexdigest()


def render_template(template: str, **context):
    with open(os.path.join("templates", template)) as f:
        template = f.read()

    for key, value in context.items():
        template = template.replace(f"{{{{ {key} }}}}", value)

    return SandboxedEnvironment().from_string(template).render(**context)
