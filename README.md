# ATS-Resume-Scanner-using-Gen-AI
In today’s competitive job market, candidates often submit their resumes through Applicant 
Tracking Systems (ATS), which are automated systems used by many companies to filter and 
assess applicants. However, resumes often fail to pass through these systems due to missing 
keywords, format errors, or irrelevant content. The ATS Resume Scanner is designed to help 
job seekers optimize their resumes by comparing them against a job description. By using a 
generative AI model, the application evaluates resumes for relevance, keyword matches, and 
overall compatibility with the job posting. To provide a tool for job seekers that evaluates 
resumes against a job description. To identify the percentage match between a resume and a 
job description based on keywords and content and also generative interview questions based 
on the resume. To offer suggestions for improving resumes to increase compatibility with 
ATS. To integrate AI-based feedback on the resume's overall quality, structure, and 
relevance to the job. 
The application uses a Google-based generative AI Gemini model to process resumes and job 
descriptions. The model identifies relevant keywords and assesses the content's alignment with 
the job requirements. Uploaded resumes (in PDF format) are converted into an image of the 
first page. This image is then encoded into base64 for processing by the AI. A user-friendly 
interface is built using Streamlit, allowing users to upload resumes, input job descriptions, and 
view results. The interface provides feedback on keyword matches, missing skills, and overall 
content evaluation. 
An accurate percentage match between a resume and job description, helping job seekers 
understand their suitability for a given role. A list of missing keywords or skills from the 
resume, along with professional suggestions for improvement.
