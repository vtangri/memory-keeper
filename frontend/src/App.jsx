import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './Layout';
import ChatInterface from './features/chat/ChatInterface';
import Dashboard from './features/dashboard/Dashboard';
import StoryDetail from './features/dashboard/StoryDetail';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<ChatInterface />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="story/:id" element={<StoryDetail />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
