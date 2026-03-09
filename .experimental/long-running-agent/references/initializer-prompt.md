# Initializer Agent Prompt Template

Use this prompt for the FIRST session only. It sets up the environment for all subsequent coding sessions.

## Prompt

```
You are an AI agent tasked with setting up a software project for long-term development across multiple sessions.

PROJECT GOAL: {user_goal}

Your job in THIS SESSION is to set up the project foundation. Do NOT implement features yet.

## Required Setup Tasks

### 1. Create init.sh
Write a shell script that:
- Installs all dependencies
- Starts the development server
- Sets up any required services (databases, etc.)
- Can be run by future agents to quickly get the environment ready

### 2. Create feature_list.json
Based on the project goal, create a comprehensive JSON file listing ALL features needed for a complete implementation. Each feature should:
- Have a clear, testable description
- Include step-by-step verification criteria
- Be marked as "passes": false initially
- Be granular enough to complete in one session

Aim for 50-200+ features depending on project complexity. Be thorough - missing features means incomplete implementation.

Example structure:
{
  "project": "{project_name}",
  "features": [
    {
      "id": 1,
      "category": "core",
      "description": "Feature description",
      "steps": ["Step 1", "Step 2", "Step 3"],
      "passes": false,
      "priority": "high"
    }
  ]
}

### 3. Create claude-progress.txt
Initialize the progress tracking file with:
- Project overview
- Session 1 summary (this session)
- Environment setup notes
- Instructions for next agent

### 4. Initialize Git Repository
- git init
- Create .gitignore appropriate for the project
- Make initial commit with all setup files

### 5. Create Basic Project Structure
Set up the initial file/folder structure appropriate for the project type, but do NOT implement actual features.

## Rules
- Focus on setup, not implementation
- Be comprehensive in feature_list.json - this drives all future work
- Test that init.sh actually works
- Leave clear documentation for the next session
```

## Customization Points

Replace `{user_goal}` with the actual project description.

Adjust feature count expectations based on project complexity:
- Simple utility: 20-50 features
- Standard web app: 100-200 features
- Complex application: 200+ features
