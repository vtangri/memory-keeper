import unittest
import asyncio
from app.services.conversation_manager import ContextManager

class TestContextManager(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.session_id = self.manager.create_session("user_123")

    def test_session_creation(self):
        self.assertIsNotNone(self.session_id)
        self.assertIn(self.session_id, self.manager.active_sessions)

    def test_topic_change(self):
        self.manager.change_topic(self.session_id, "childhood")
        ctx = self.manager.get_session(self.session_id)
        self.assertEqual(ctx.current_topic, "childhood")

    def test_interaction_flow(self):
        # Async test wrapper
        async def run_flow():
            response = await self.manager.process_user_input(self.session_id, "I liked playing hide and seek.")
            self.assertTrue(len(response) > 0)
            ctx = self.manager.get_session(self.session_id)
            self.assertEqual(len(ctx.history), 2) # User + AI
            self.assertEqual(ctx.history[0]["role"], "user")
            self.assertEqual(ctx.history[1]["role"], "ai")
        
        asyncio.run(run_flow())

if __name__ == '__main__':
    unittest.main()
