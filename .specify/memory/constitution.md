
## IMPLEMENTATION WORKFLOW
1. **Read** constitution.md and speckit.specify
2. **Create** speckit.plan based on specifications
3. **Break down** into speckit.tasks
4. **Generate** code for each task
5. **Test** each implementation
6. **Update specs** if issues found (NOT the code)

## TECHNICAL CONSTRAINTS
- Python 3.12+ (Windows compatible)
- In-memory storage only (Python lists/dictionaries)
- No external dependencies (except pytest for testing)
- Type hints required for all functions
- Console menu interface (1-6 options)
- UTF-8 encoding support

## REPOSITORY STRUCTURE
- phase-1/: Python 3.12 console app (completed)
- phase-2/: Full-stack web app (Next.js + FastAPI + Neon)
- phase-3/: AI Chatbot (Future)
- phase-4/: Kubernetes deployment (Future)
- phase-5/: Cloud deployment (Future)

## PHASE 2 REQUIREMENTS
- Python 3.13+ with UV package manager
- Next.js 16+ frontend
- FastAPI backend with SQLModel
- Neon PostgreSQL database
- Better Auth with JWT tokens
- Reusable Intelligence: Agent Skills + Subagents (+200 bonus)
- MCP server setup for task tools

## FIRST PROMPT TO EXECUTE
After reading this file, please:
1. Review the constitution and specifications
2. Create speckit.plan for Phase I implementation
3. Structure the plan according to the 5 features

Remember: I cannot write code manually. Guide me through the spec-driven process.