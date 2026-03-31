import { Routes, Route, Navigate } from "react-router-dom";
import RequireAuth from "./RequireAuth.jsx";
import LevelsPage from "@/features/levels/pages/LevelsPage.jsx";
import TopicsPage from "@/features/topics/pages/TopicsPage.jsx";
import TopicDetailPage from "@/features/topic/pages/TopicDetailPage.jsx";
import LearnPage from "@/features/topic/pages/LearnPage.jsx";
import ExamPage from "@/features/exam/pages/ExamPage.jsx";
import PracticePage from "@/features/practice/pages/PracticePage.jsx";
import LoginPage from "@/features/auth/pages/LoginPage.jsx";
import RegisterPage from "@/features/auth/pages/RegisterPage.jsx";
import ForgotPasswordPage from "@/features/auth/pages/ForgotPasswordPage.jsx";
import ResetPasswordPage from "@/features/auth/pages/ResetPasswordPage.jsx";

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/forgot-password" element={<ForgotPasswordPage />} />
      <Route path="/reset-password" element={<ResetPasswordPage />} />
      <Route element={<RequireAuth />}>
        <Route path="/" element={<LevelsPage />} />
        <Route path="/level/:levelId" element={<TopicsPage />} />
        <Route path="/topic/:topicId" element={<TopicDetailPage />} />
        <Route path="/topic/:topicId/learn" element={<LearnPage />} />
        <Route path="/topic/:topicId/exam" element={<ExamPage />} />
        <Route path="/practice" element={<PracticePage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
