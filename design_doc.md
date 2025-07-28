# Cover Letter Generator MVP - Design Document

## Overview
An LLM-powered web application that generates personalized cover letters by analyzing user profiles and job descriptions. Built with Flask backend and vanilla JavaScript frontend.

## Core Functionality
The system creates custom cover letters through an iterative process:
1. **Profile Creation** - Streamlined 3-step user onboarding
2. **Job Analysis** - Extract requirements from job postings  
3. **Letter Generation** - Create tailored cover letters
4. **Revision Loop** - Iterative improvement with context memory

## User Flow

### Profile Creation (One-time Setup)
1. **Target Job Type** - User specifies what type of role they're seeking
2. **Resume Upload** - Upload existing resume (PDF/DOCX/TXT)
3. **Self Description** - Brief description of themselves (personality, goals, achievements)

### Cover Letter Generation (Per Job Application)
1. **Job Input** - URL scraping or copy/paste job description
2. **Analysis** - System identifies key requirements and matches to profile
3. **Generation** - Creates initial cover letter draft
4. **Review & Revision** - User can request changes with context memory
5. **Export** - Download as PDF or DOCX

## Technical Architecture

### Backend (Python Flask)
```
/api/profile
  POST /create - Create user profile
  GET /{user_id} - Retrieve profile
  PUT /{user_id} - Update profile

/api/jobs
  POST /analyze - Analyze job description (URL or text)
  GET /{job_id} - Retrieve parsed job data

/api/letters
  POST /generate - Generate cover letter
  POST /{letter_id}/revise - Revise existing letter
  GET /{letter_id} - Retrieve letter
  POST /{letter_id}/export - Export as PDF/DOCX
```

### Frontend (Vanilla JavaScript)
- Single Page Application
- Progressive form for profile creation
- Job input interface (URL + textarea)
- Cover letter editor with revision interface
- Export functionality

### Database Schema
```sql
users
- id, email, created_at

profiles  
- user_id, target_job_type, resume_text, self_description, extracted_data (JSON)

jobs
- id, user_id, title, company, description, requirements (JSON), created_at

cover_letters
- id, user_id, job_id, content, version, created_at

revisions
- id, letter_id, user_feedback, revised_content, created_at
```

## LLM Chain Architecture (LangChain + OpenAI)

### 1. Profile Processing Chain
- **Input**: Uploaded resume file + self description
- **Model**: GPT-4o-mini (cost-effective for extraction)
- **Output**: Structured profile data (skills, experience, achievements, tone)

### 2. Job Analysis Chain  
- **Input**: Job description (scraped or pasted)
- **Model**: GPT-4o-mini (extraction task)
- **Output**: Key requirements, required skills, company culture, role responsibilities

### 3. Profile-Job Matching Chain
- **Input**: Structured profile + job requirements
- **Model**: GPT-4o-mini (analysis task)
- **Output**: Match analysis, relevant experiences to highlight, gaps to address

### 4. Cover Letter Generation Chain
- **Input**: Profile + job analysis + match data
- **Model**: GPT-4o (creative generation)
- **Output**: Personalized cover letter draft

### 5. Revision Chain (with Memory)
- **Input**: Previous letter + user feedback + conversation history
- **Model**: GPT-4o (creative revision)
- **Output**: Revised letter maintaining context

## Key Features

### Gap Analysis & Suggestions
- Flag missing skills/experience compared to job requirements
- Suggest profile enhancements
- Highlight strongest matching points

### Web Scraping
- Extract job descriptions from URLs
- Fallback to copy/paste input
- Clean and structure job posting data

### Memory & Context
- Maintain conversation history for revisions
- Remember user preferences and feedback patterns
- Context-aware improvements

## File Structure
```
/
├── app.py                 # Flask application
├── models/
│   ├── profile.py         # Profile data models
│   ├── job.py            # Job analysis models  
│   └── letter.py         # Cover letter models
├── chains/
│   ├── profile_chain.py   # Profile processing
│   ├── job_chain.py      # Job analysis
│   ├── match_chain.py    # Profile-job matching
│   ├── generate_chain.py # Letter generation
│   └── revise_chain.py   # Revision with memory
├── utils/
│   ├── scraper.py        # Web scraping utilities
│   ├── file_parser.py    # Resume file parsing
│   └── export.py         # PDF/DOCX generation
├── static/
│   ├── js/
│   │   ├── app.js        # Main application
│   │   ├── profile.js    # Profile creation
│   │   └── generator.js  # Letter generation UI
│   └── css/
│       └── styles.css    # Application styles
└── templates/
    └── index.html        # Single page application
```

## Dependencies
```
Flask
LangChain
OpenAI API
BeautifulSoup4 (web scraping)
PyPDF2/python-docx (file parsing)
ReportLab (PDF generation)
python-docx (DOCX generation)
```

## Future Enhancements (Post-MVP)

### Technical Upgrades
- **LiteLLM Integration** - Support multiple LLM providers
- **Local Models** - CPU-optimized models for extraction tasks
- **Chrome Extension** - One-click job application processing
- **Resume Generation** - Expand to full resume creation

### Advanced Features  
- **A/B Testing** - Multiple letter variations
- **Industry Templates** - Role-specific letter structures
- **Company Research** - Integrate company background data
- **Application Tracking** - Monitor application status
- **Analytics Dashboard** - Success rate tracking

## MVP Success Metrics
- User can create profile in under 3 minutes
- Generate quality cover letter in under 2 minutes
- Revision process feels conversational and contextual
- Letters feel personalized, not generic AI-generated
- System identifies and addresses profile-job gaps effectively

## Development Phases
1. **Phase 1**: Basic profile creation and storage
2. **Phase 2**: Job description analysis and web scraping  
3. **Phase 3**: Cover letter generation chain
4. **Phase 4**: Revision system with memory
5. **Phase 5**: Export functionality and UI polish

---

## Notes for Future Development

### Model Alternatives (Future Consideration)
- **LiteLLM Integration**: Replace direct OpenAI calls with LiteLLM for provider flexibility
- **Local Model Options**: 
  - Llama 3.2 3B for extraction tasks
  - Phi-3-mini for lightweight processing
  - Consider CPU-optimized models for cost reduction on extraction chains

### Architecture Considerations
- Build model-agnostic interfaces from start
- Implement token counting and cost estimation
- Design for easy model swapping without code changes
- Consider batch processing for efficiency at scale