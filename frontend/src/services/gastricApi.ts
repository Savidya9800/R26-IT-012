// frontend/src/services/gastricApi.ts

const API_URL = "http://127.0.0.1:8000/api/gastric/analyze";

export interface GastricSymptomData {
  pain_after_meals: boolean;
  spicy_food_trigger: boolean;
  // Add other symptoms as needed
}

export interface StudentPrescriptionData {
  medication?: string;
  notes?: string;
}

export interface GastricAnalysisResponse {
  status: string;
  symptom_data: any;
  ai_diagnosis: {
    condition: string;
    confidence: number;
    severity: string;
    gradcam_image?: string;
  };
  educational_feedback: string;
}

export const analyzeGastricData = async (
  symptoms: GastricSymptomData,
  imageFile: File,
  studentPrescription?: StudentPrescriptionData
): Promise<GastricAnalysisResponse> => {
  const formData = new FormData();
  
  formData.append("image", imageFile);
  formData.append("symptoms", JSON.stringify(symptoms));
  
  if (studentPrescription) {
    formData.append("student_prescription", JSON.stringify(studentPrescription));
  }

  const response = await fetch(API_URL, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Failed to analyze gastric data");
  }

  return response.json();
};