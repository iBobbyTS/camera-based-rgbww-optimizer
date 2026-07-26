import ast
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ProjectContextStructureTests(unittest.TestCase):
    def test_progressive_skill_and_docs_routes(self):
        skill = ROOT / ".agents/skills/camera-based-rgbww-optimizer/SKILL.md"
        readme = (ROOT / "docs/README.md").read_text(encoding="utf-8")
        skill_text = skill.read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertLessEqual(skill.stat().st_size, 12_000)
        for heading in ("## Scope", "## Role and Ownership Core", "## Core Safety and Runtime Rules", "## Progressive Routing"):
            self.assertIn(heading, skill_text)
        self.assertIn("docs/local-lab-connection-boundary.md", skill_text)
        self.assertIn("docs/engineering/p7-td-b-contract-history.md", skill_text)
        self.assertIn("local-lab-connection-boundary.md", readme)
        self.assertLess(agents.index("## Local Lab Scope"), agents.index("## Language"))

    def test_ray_public_protocol_default_and_private_override_contract(self):
        path = ROOT / "src/camera_based_rgbww_optimizer/control/ray120c.py"
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        default_assignment = next(
            node for node in tree.body
            if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "DEFAULT_OPENAPI_SECRET" for target in node.targets)
        )
        self.assertEqual(ast.literal_eval(default_assignment.value), "9veqiL0G0EUOviwzL1prPc0iGIGUJtbzSaPYQfgfyxM=")
        self.assertNotIn('add_argument("--secret"', source)
        settings = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "OpenAPISettings")
        secret_field = next(
            node for node in settings.body
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "secret"
        )
        self.assertIsNotNone(secret_field.value)
        self.assertIn("repr=False", ast.unparse(secret_field.value))
        generate = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "generate_token")
        self.assertEqual(len(generate.args.defaults), 1)
        self.assertEqual(ast.unparse(generate.args.defaults[0]), "DEFAULT_OPENAPI_SECRET")

        boundary = (ROOT / "docs/local-lab-connection-boundary.md").read_text(encoding="utf-8")
        readme = (ROOT / "docs/README.md").read_text(encoding="utf-8")
        skill = (ROOT / ".agents/skills/camera-based-rgbww-optimizer/SKILL.md").read_text(encoding="utf-8")
        for text in (boundary, readme, skill):
            self.assertIn("Human-classified public shared protocol default", text)
            self.assertIn("optional explicit override", text)
            self.assertIn("private runtime value", text)
            self.assertIn("not an external-vendor verification claim", text)
            self.assertNotIn("There is no built-in default", text)
            self.assertNotIn("AMARAN_OPENAPI_SECRET` in the user-owned process environment", text)


if __name__ == "__main__":
    unittest.main()
