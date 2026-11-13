import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import TextToVideo from "./pages/TextToVideo.jsx";
import TextToImage from "./pages/TextToImage.jsx";
import ImageToVideo from "./pages/ImageToVideo.jsx";
import History from "./pages/History.jsx";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="text-to-image" element={<TextToImage />} />
        <Route path="text-to-video" element={<TextToVideo />} />
        <Route path="image-to-video" element={<ImageToVideo />} />
        <Route path="projects" element={<History />} />
        <Route path="*" element={<Dashboard />} />
      </Route>
    </Routes>
  );
}
