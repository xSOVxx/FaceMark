import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';
import { useParams, useNavigate } from 'react-router-dom';
import { markAttendance } from '../api/professor';
import { Camera, CheckCircle, XCircle, ArrowLeft } from 'lucide-react';

const Attendance = () => {
    const { classId } = useParams();
    const webcamRef = useRef(null);
    const [imgSrc, setImgSrc] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const navigate = useNavigate();

    const capture = useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        setImgSrc(imageSrc);
    }, [webcamRef]);

    const retake = () => {
        setImgSrc(null);
        setResult(null);
    };

    const handleSubmit = async () => {
        if (!imgSrc) return;
        setLoading(true);
        try {
            // Convert base64 to blob
            const res = await fetch(imgSrc);
            const blob = await res.blob();
            const file = new File([blob], "attendance.jpg", { type: "image/jpeg" });

            // Assuming professor ID is 1 for now or get from context
            // In real app, backend should infer from token or context should provide it
            const professorId = 1;

            const data = await markAttendance(classId, professorId, file);
            setResult(data);
        } catch (error) {
            console.error("Error marking attendance", error);
            alert("Failed to mark attendance");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto">
            <button onClick={() => navigate('/professor')} className="flex items-center text-gray-600 mb-6 hover:text-gray-900">
                <ArrowLeft className="w-5 h-5 mr-1" /> Back to Dashboard
            </button>

            <div className="bg-white p-6 rounded-lg shadow-lg">
                <h2 className="text-2xl font-bold mb-6 text-center">Take Attendance - Class {classId}</h2>

                <div className="flex flex-col items-center space-y-6">
                    {!imgSrc ? (
                        <div className="relative rounded-lg overflow-hidden shadow-md">
                            <Webcam
                                audio={false}
                                ref={webcamRef}
                                screenshotFormat="image/jpeg"
                                width={640}
                                height={480}
                                className="rounded-lg"
                            />
                        </div>
                    ) : (
                        <div className="relative rounded-lg overflow-hidden shadow-md">
                            <img src={imgSrc} alt="Captured" className="rounded-lg" />
                        </div>
                    )}

                    <div className="flex space-x-4">
                        {!imgSrc ? (
                            <button
                                onClick={capture}
                                className="bg-blue-600 text-white px-6 py-3 rounded-full hover:bg-blue-700 flex items-center shadow-lg transform hover:scale-105 transition"
                            >
                                <Camera className="w-6 h-6 mr-2" /> Capture
                            </button>
                        ) : (
                            <>
                                <button
                                    onClick={retake}
                                    className="bg-gray-500 text-white px-6 py-3 rounded-full hover:bg-gray-600 flex items-center shadow-lg"
                                >
                                    <XCircle className="w-6 h-6 mr-2" /> Retake
                                </button>
                                <button
                                    onClick={handleSubmit}
                                    disabled={loading}
                                    className="bg-green-600 text-white px-6 py-3 rounded-full hover:bg-green-700 flex items-center shadow-lg"
                                >
                                    {loading ? 'Processing...' : (
                                        <>
                                            <CheckCircle className="w-6 h-6 mr-2" /> Submit
                                        </>
                                    )}
                                </button>
                            </>
                        )}
                    </div>

                    {result && (
                        <div className="mt-8 w-full">
                            <h3 className="text-xl font-semibold mb-4 text-center">Attendance Result</h3>
                            <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                                <p><strong>Date:</strong> {result.fecha}</p>
                                <p><strong>Time:</strong> {result.hora}</p>
                                <h4 className="font-semibold mt-4 mb-2">Present Students:</h4>
                                <ul className="list-disc list-inside">
                                    {result.detalles && result.detalles.length > 0 ? (
                                        result.detalles.map((d, idx) => (
                                            <li key={idx} className="text-green-700">{d.alumno.nombre} ({d.alumno.codigo})</li>
                                        ))
                                    ) : (
                                        <li className="text-gray-500">No students recognized.</li>
                                    )}
                                </ul>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Attendance;
