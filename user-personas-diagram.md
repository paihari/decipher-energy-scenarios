# Swiss Energy Scenarios Decipher System - User Personas

## User Persona Flow Diagram

```mermaid
flowchart TD
    A[Swiss Energy Scenarios Decipher System] --> B{User Persona Detection}
    
    B --> C[🏠 Citizen]
    B --> D[📰 Journalist]
    B --> E[🎓 Student]
    B --> F[🏛️ Policymaker]
    
    C --> C1[Simple Explanations]
    C --> C2[Practical Applications]
    C --> C3[Everyday Impact]
    
    D --> D1[Facts with Context]
    D --> D2[Story Angles]
    D --> D3[Public Interest]
    
    E --> E1[Educational Content]
    E --> E2[Detailed Explanations]
    E --> E3[Learning Objectives]
    
    F --> F1[Comprehensive Analysis]
    F --> F2[Policy Implications]
    F --> F3[Implementation Details]
    
    C1 --> G[Tailored Response]
    C2 --> G
    C3 --> G
    D1 --> G
    D2 --> G
    D3 --> G
    E1 --> G
    E2 --> G
    E3 --> G
    F1 --> G
    F2 --> G
    F3 --> G
    
    G --> H[🌍 Multilingual Output]
    H --> I[EN/DE/FR/IT]
    
    style A fill:#e1f5fe
    style B fill:#fff3e0
    style C fill:#e8f5e8
    style D fill:#fff8e1
    style E fill:#f3e5f5
    style F fill:#e0f2f1
    style G fill:#fce4ec
    style H fill:#f1f8e9
```

## Persona-Focused Diagram

```mermaid
graph TB
    subgraph "🏠 Citizen Persona"
        C1[Energy Bill Impact]
        C2[Home Efficiency Tips]
        C3[Climate Actions]
    end
    
    subgraph "📰 Journalist Persona"
        J1[Breaking News Angles]
        J2[Data Visualization]
        J3[Expert Quotes]
    end
    
    subgraph "🎓 Student Persona"
        S1[Research Methods]
        S2[Technical Details]
        S3[Case Studies]
    end
    
    subgraph "🏛️ Policymaker Persona"
        P1[Economic Impact]
        P2[Implementation Roadmap]
        P3[Regulatory Framework]
    end
    
    QUERY[Energy Question] --> SYSTEM[Swiss Energy System]
    SYSTEM --> C1
    SYSTEM --> J1
    SYSTEM --> S1
    SYSTEM --> P1
    
    style QUERY fill:#ffcdd2
    style SYSTEM fill:#e1f5fe
```

## User Personas Overview

### 👥 **User Types**
The system adapts responses based on 4 user types:

1. **🏠 Citizen** 
   - **Response Style:** Simple, practical explanations
   - **Focus:** Everyday impact, energy bills, home efficiency
   - **Example:** "How will the energy transition affect my heating costs?"

2. **📰 Journalist** 
   - **Response Style:** Facts with context and story angles
   - **Focus:** Breaking news, data visualization, expert perspectives
   - **Example:** "What's the latest data on renewable energy adoption in Switzerland?"

3. **🎓 Student** 
   - **Response Style:** Educational content with detailed explanations
   - **Focus:** Research methods, technical details, case studies
   - **Example:** "Explain the methodology used in Swiss energy scenario modeling"

4. **🏛️ Policymaker** 
   - **Response Style:** Comprehensive analysis with implications
   - **Focus:** Economic impact, implementation roadmaps, regulatory frameworks
   - **Example:** "What are the policy implications of the ZERO scenario by 2030?"

### 🌍 **Multilingual Support**
All personas receive responses in their preferred language:
- **🇬🇧 English** - International communication
- **🇩🇪 Deutsch** - German-speaking Switzerland
- **🇫🇷 Français** - French-speaking Switzerland  
- **🇮🇹 Italiano** - Italian-speaking Switzerland

The system automatically detects query language and provides responses in the user's selected interface language, ensuring accessibility across all Swiss linguistic regions.