"""Seed data generation script for PromptLab.

This script populates the API with 50 realistic prompts for testing and demo purposes.

Usage:
    python seed_data.py
"""

from app.models import Prompt, Collection, get_current_time
from app.storage import storage


def create_collections():
    """Create sample collections."""
    collections_data = [
        {"name": "Development", "description": "Prompts for software development tasks"},
        {"name": "Content Writing", "description": "Prompts for creative and technical writing"},
        {"name": "Data Analysis", "description": "Prompts for data analysis and visualization"},
        {"name": "Marketing", "description": "Prompts for marketing and copywriting"},
        {"name": "Education", "description": "Prompts for teaching and learning"},
        {"name": "Design", "description": "Prompts for UI/UX design tasks"},
    ]
    
    collection_ids = {}
    for col_data in collections_data:
        col = Collection(**col_data)
        created = storage.create_collection(col)
        collection_ids[col_data["name"]] = created.id
    
    return collection_ids


def create_prompts(collection_ids):
    """Create 50 realistic prompts."""
    prompts_data = [
        # Development Prompts (10)
        {
            "title": "Code Review Assistant",
            "content": "Review the following code and provide feedback on:\n1. Code quality and readability\n2. Potential bugs or performance issues\n3. Best practices and improvements\n\nCode:\n```\n{{code}}\n```",
            "description": "AI-assisted code review tool",
            "collection": "Development"
        },
        {
            "title": "Bug Debugging Helper",
            "content": "I'm getting this error: {{error}}\n\nHere's my code:\n```\n{{code}}\n```\n\nHelp me understand what's wrong and how to fix it.",
            "description": "Debug errors with AI assistance",
            "collection": "Development"
        },
        {
            "title": "Documentation Generator",
            "content": "Generate comprehensive documentation for this function:\n```\n{{code}}\n```\n\nInclude:\n- Function purpose\n- Parameters and return types\n- Usage examples\n- Edge cases",
            "description": "Auto-generate code documentation",
            "collection": "Development"
        },
        {
            "title": "SQL Query Optimizer",
            "content": "Optimize this SQL query for performance:\n```\n{{query}}\n```\n\nContext: {{context}}\n\nProvide:\n1. Optimized query\n2. Explanation of changes\n3. Performance impact",
            "description": "Optimize database queries",
            "collection": "Development"
        },
        {
            "title": "API Endpoint Designer",
            "content": "Design REST API endpoints for: {{feature}}\n\nInclude:\n- Endpoint paths and methods\n- Request/response schemas\n- Error handling\n- Authentication requirements",
            "description": "Design RESTful API endpoints",
            "collection": "Development"
        },
        {
            "title": "Testing Strategy Creator",
            "content": "Create a comprehensive testing strategy for: {{feature}}\n\nInclude:\n- Unit tests\n- Integration tests\n- Test cases and edge cases\n- Mock data requirements",
            "description": "Plan testing strategy",
            "collection": "Development"
        },
        {
            "title": "Refactoring Suggestions",
            "content": "Suggest refactoring improvements for this code:\n```\n{{code}}\n```\n\nFocus on:\n- DRY principle\n- Code complexity\n- Maintainability",
            "description": "Improve code structure",
            "collection": "Development"
        },
        {
            "title": "Architecture Review",
            "content": "Review the architecture of {{project}}:\n\nCurrent structure: {{structure}}\n\nProvide:\n1. Strengths\n2. Weaknesses\n3. Improvement recommendations",
            "description": "Evaluate system architecture",
            "collection": "Development"
        },
        {
            "title": "Dependency Analyzer",
            "content": "Analyze these dependencies for my {{language}} project:\n{{dependencies}}\n\nProvide:\n- Security concerns\n- Performance impact\n- Alternatives",
            "description": "Analyze project dependencies",
            "collection": "Development"
        },
        {
            "title": "Git Commit Message Writer",
            "content": "Write a professional git commit message for these changes:\n{{changes}}\n\nFormat: conventional commits style",
            "description": "Generate commit messages",
            "collection": "Development"
        },
        
        # Content Writing Prompts (10)
        {
            "title": "Blog Post Outline Generator",
            "content": "Create an outline for a blog post about: {{topic}}\n\nTarget audience: {{audience}}\nDesired length: {{word_count}} words\n\nInclude:\n- Main sections\n- Key points per section\n- Call-to-action",
            "description": "Outline blog content",
            "collection": "Content Writing"
        },
        {
            "title": "Social Media Caption Writer",
            "content": "Write engaging social media captions for:\n\nPlatform: {{platform}}\nContent: {{content}}\nTone: {{tone}}\nHashtags: {{include_hashtags}}\n\nMake it compelling and on-brand.",
            "description": "Create social media posts",
            "collection": "Content Writing"
        },
        {
            "title": "Email Copy Creator",
            "content": "Write an email for: {{email_type}}\n\nContext:\n- Recipient: {{recipient}}\n- Purpose: {{purpose}}\n- Company tone: {{tone}}\n\nInclude:\n- Subject line\n- Body\n- Call-to-action",
            "description": "Create email marketing content",
            "collection": "Content Writing"
        },
        {
            "title": "Product Description Writer",
            "content": "Write a compelling product description for:\n\nProduct: {{product}}\nFeatures: {{features}}\nTarget market: {{target}}\nPrice point: {{price}}\n\nMake it sell!",
            "description": "Write product descriptions",
            "collection": "Content Writing"
        },
        {
            "title": "Press Release Generator",
            "content": "Create a press release for: {{news}}\n\nKey details:\n- Date: {{date}}\n- Company: {{company}}\n- Impact: {{impact}}\n\nInclude standard PR format.",
            "description": "Generate press releases",
            "collection": "Content Writing"
        },
        {
            "title": "Headline Generator",
            "content": "Generate 10 compelling headlines for:\n\nTopic: {{topic}}\nFormat: {{format}}\nAudience: {{audience}}\n\nMake them click-worthy and accurate.",
            "description": "Create attention-grabbing headlines",
            "collection": "Content Writing"
        },
        {
            "title": "Content Repurposing Assistant",
            "content": "Repurpose this content:\n\nOriginal content: {{content}}\nFormats to create: {{formats}}\n\nAdapt for each platform's best practices.",
            "description": "Adapt content for multiple formats",
            "collection": "Content Writing"
        },
        {
            "title": "SEO Optimization Assistant",
            "content": "Optimize this content for SEO:\n\nOriginal content: {{content}}\nTarget keywords: {{keywords}}\nTarget audience: {{audience}}\n\nProvide:\n- Optimized version\n- Meta description\n- Internal link suggestions",
            "description": "Optimize for search engines",
            "collection": "Content Writing"
        },
        {
            "title": "Speech Writer",
            "content": "Write a speech about: {{topic}}\n\nDetails:\n- Length: {{duration}} minutes\n- Audience: {{audience}}\n- Tone: {{tone}}\n- Key messages: {{messages}}\n\nInclude opening, body, and conclusion.",
            "description": "Compose speeches",
            "collection": "Content Writing"
        },
        {
            "title": "Story Ideation",
            "content": "Generate story ideas for: {{genre}}\n\nRequirements:\n- Setting: {{setting}}\n- Characters: {{characters}}\n- Tone: {{tone}}\n\nProvide 5 unique plot ideas.",
            "description": "Brainstorm creative stories",
            "collection": "Content Writing"
        },
        
        # Data Analysis Prompts (10)
        {
            "title": "Data Visualization Recommender",
            "content": "What's the best way to visualize this data?\n\nData type: {{type}}\nVariables: {{variables}}\nGoal: {{goal}}\nAudience: {{audience}}\n\nRecommend visualization types with justification.",
            "description": "Recommend chart types",
            "collection": "Data Analysis"
        },
        {
            "title": "Statistical Analysis Guide",
            "content": "Analyze this dataset:\n\nData: {{data}}\nQuestion: {{question}}\n\nProvide:\n- Relevant statistics\n- Interpretation\n- Confidence levels\n- Limitations",
            "description": "Perform statistical analysis",
            "collection": "Data Analysis"
        },
        {
            "title": "Trend Analysis Assistant",
            "content": "Analyze trends in this data:\n\nDataset: {{data}}\nTime period: {{period}}\n\nIdentify:\n- Overall trends\n- Seasonal patterns\n- Anomalies\n- Predictions",
            "description": "Identify data trends",
            "collection": "Data Analysis"
        },
        {
            "title": "Report Generator",
            "content": "Generate an analysis report for:\n\nData: {{data}}\nStakeholders: {{stakeholders}}\nFocus areas: {{areas}}\n\nInclude executive summary and recommendations.",
            "description": "Create data reports",
            "collection": "Data Analysis"
        },
        {
            "title": "A/B Test Analyzer",
            "content": "Analyze A/B test results:\n\nVariant A: {{variant_a}}\nVariant B: {{variant_b}}\nMetrics: {{metrics}}\nSample size: {{size}}\n\nProvide statistical significance and recommendation.",
            "description": "Analyze A/B test results",
            "collection": "Data Analysis"
        },
        {
            "title": "Anomaly Detection",
            "content": "Identify anomalies in this dataset:\n\nData: {{data}}\nNormal range: {{range}}\n\nFlag unusual patterns and investigate causes.",
            "description": "Find data anomalies",
            "collection": "Data Analysis"
        },
        {
            "title": "Correlation Analyzer",
            "content": "Analyze correlations between:\n\nVariables: {{variables}}\nDataset: {{data}}\n\nProvide:\n- Correlation coefficients\n- Significance levels\n- Causation possibilities",
            "description": "Find data relationships",
            "collection": "Data Analysis"
        },
        {
            "title": "Forecasting Model",
            "content": "Create a forecast for: {{metric}}\n\nHistorical data: {{data}}\nForecast period: {{period}}\nConfidence level: {{level}}\n\nProvide model recommendations and projections.",
            "description": "Forecast future values",
            "collection": "Data Analysis"
        },
        {
            "title": "Data Quality Checker",
            "content": "Evaluate data quality for:\n\nDataset: {{data}}\n\nAssess:\n- Completeness\n- Accuracy\n- Consistency\n- Validity\n\nProvide improvement recommendations.",
            "description": "Assess data quality",
            "collection": "Data Analysis"
        },
        {
            "title": "Segmentation Analyzer",
            "content": "Suggest data segments for:\n\nData: {{data}}\nBusiness goal: {{goal}}\nVariables available: {{variables}}\n\nProvide segment definitions and characteristics.",
            "description": "Identify data segments",
            "collection": "Data Analysis"
        },
        
        # Marketing Prompts (10)
        {
            "title": "Campaign Strategy Builder",
            "content": "Create a marketing campaign strategy for:\n\nProduct: {{product}}\nTarget audience: {{audience}}\nBudget: {{budget}}\nTimeframe: {{timeframe}}\n\nInclude channels, messaging, and KPIs.",
            "description": "Plan marketing campaigns",
            "collection": "Marketing"
        },
        {
            "title": "Customer Persona Generator",
            "content": "Generate detailed customer personas for: {{product}}\n\nInclude:\n- Demographics\n- Psychographics\n- Pain points\n- Goals\n- Behaviors",
            "description": "Create customer profiles",
            "collection": "Marketing"
        },
        {
            "title": "Funnel Optimizer",
            "content": "Optimize our marketing funnel:\n\nCurrent funnel: {{funnel}}\nConversion rates: {{rates}}\nBottlenecks: {{bottlenecks}}\n\nProvide improvement recommendations.",
            "description": "Improve conversion funnel",
            "collection": "Marketing"
        },
        {
            "title": "Competitor Analysis",
            "content": "Analyze competitive landscape for: {{product}}\n\nCompetitors: {{competitors}}\n\nEvaluate:\n- Strengths/weaknesses\n- Pricing\n- Marketing approach\n- Market positioning",
            "description": "Analyze competitors",
            "collection": "Marketing"
        },
        {
            "title": "Brand Messaging Creator",
            "content": "Create brand messaging for: {{brand}}\n\nBrand values: {{values}}\nTarget market: {{market}}\nUnique value: {{value}}\n\nDefine tagline, positioning, and key messages.",
            "description": "Develop brand messaging",
            "collection": "Marketing"
        },
        {
            "title": "Pricing Strategy Advisor",
            "content": "Recommend pricing strategy for: {{product}}\n\nCost: {{cost}}\nMarket: {{market}}\nCompetition: {{competition}}\nValue perception: {{perception}}\n\nAnalyze options and recommend strategy.",
            "description": "Optimize pricing strategy",
            "collection": "Marketing"
        },
        {
            "title": "Influencer Matching",
            "content": "Find influencers for: {{product}}\n\nTarget audience: {{audience}}\nBudget: {{budget}}\nGoal: {{goal}}\n\nProvide profile recommendations and reasoning.",
            "description": "Find relevant influencers",
            "collection": "Marketing"
        },
        {
            "title": "Content Calendar Planner",
            "content": "Create a content calendar for {{channel}}\n\nTimeperiod: {{period}}\nTopics: {{topics}}\nFrequency: {{frequency}}\n\nProvide schedule and content ideas.",
            "description": "Plan content schedule",
            "collection": "Marketing"
        },
        {
            "title": "Customer Journey Mapper",
            "content": "Map the customer journey for: {{product}}\n\nKey touchpoints: {{touchpoints}}\n\nIdentify:\n- Awareness stage content\n- Consideration content\n- Decision content\n- Retention strategies",
            "description": "Map customer experience",
            "collection": "Marketing"
        },
        {
            "title": "Referral Program Designer",
            "content": "Design a referral program for: {{product}}\n\nCurrent customers: {{customers}}\nTarget growth: {{growth}}\nBudget: {{budget}}\n\nStructure incentives and mechanics.",
            "description": "Create referral program",
            "collection": "Marketing"
        },
    ]
    
    # Shuffle and add remaining prompts for Education and Design
    education_prompts = [
        {
            "title": "Lesson Plan Generator",
            "content": "Create a lesson plan for: {{topic}}\n\nGrade level: {{grade}}\nDuration: {{duration}}\nObjectives: {{objectives}}\n\nInclude activities, assessments, and resources.",
            "description": "Design educational lessons",
            "collection": "Education"
        },
        {
            "title": "Quiz Creator",
            "content": "Create a quiz about: {{topic}}\n\nDifficulty: {{difficulty}}\nNumber of questions: {{count}}\n\nProvide questions and answer key with explanations.",
            "description": "Generate assessment quizzes",
            "collection": "Education"
        },
        {
            "title": "Study Guide Writer",
            "content": "Write a study guide for: {{subject}}\n\nKey concepts: {{concepts}}\nExam type: {{exam_type}}\n\nInclude summaries, practice problems, and tips.",
            "description": "Create study materials",
            "collection": "Education"
        },
        {
            "title": "Explanation Simplifier",
            "content": "Explain {{concept}} in simple terms.\n\nContext: {{context}}\nTarget audience: {{age}}\n\nUse analogies and examples.",
            "description": "Simplify complex concepts",
            "collection": "Education"
        },
        {
            "title": "Research Paper Guide",
            "content": "Guide for writing a research paper on: {{topic}}\n\nInclude:\n- Research strategies\n- Structure guidelines\n- Citation format\n- Common pitfalls",
            "description": "Guide research writing",
            "collection": "Education"
        },
    ]
    
    design_prompts = [
        {
            "title": "UI Layout Suggester",
            "content": "Suggest UI layout for: {{app}}\n\nFeatures: {{features}}\nTarget users: {{users}}\nPlatform: {{platform}}\n\nProvide layout wireframe suggestions.",
            "description": "Design interface layouts",
            "collection": "Design"
        },
        {
            "title": "Color Palette Generator",
            "content": "Generate color palette for: {{brand/app}}\n\nBrand personality: {{personality}}\nUse cases: {{uses}}\nAccessibility requirements: {{requirements}}\n\nProvide palette with usage guidelines.",
            "description": "Create color schemes",
            "collection": "Design"
        },
        {
            "title": "Typography Advisor",
            "content": "Recommend typography for: {{project}}\n\nStyle: {{style}}\nReadability needs: {{needs}}\nBrand alignment: {{brand}}\n\nSuggest fonts with pairing recommendations.",
            "description": "Select appropriate fonts",
            "collection": "Design"
        },
        {
            "title": "Accessibility Reviewer",
            "content": "Review accessibility of: {{design}}\n\nCurrent design: {{description}}\n\nCheck:\n- Contrast ratios\n- Font sizes\n- Navigation\n- Alternative text\n\nProvide recommendations.",
            "description": "Ensure design accessibility",
            "collection": "Design"
        },
        {
            "title": "Design System Creator",
            "content": "Create a design system for: {{organization}}\n\nExisting elements: {{elements}}\nScale: {{scale}}\n\nDefine components, patterns, and guidelines.",
            "description": "Build design systems",
            "collection": "Design"
        },
    ]
    
    prompts_data.extend(education_prompts)
    prompts_data.extend(design_prompts)
    
    # Create prompts
    created_count = 0
    for prompt_data in prompts_data:
        collection = prompt_data.pop("collection")
        collection_id = collection_ids.get(collection)
        
        prompt = Prompt(
            title=prompt_data["title"],
            content=prompt_data["content"],
            description=prompt_data.get("description", ""),
            collection_id=collection_id
        )
        
        storage.create_prompt(prompt)
        created_count += 1
    
    return created_count


def main():
    """Main function to seed the database."""
    print("🌱 Seeding PromptLab database...")
    print()
    
    # Clear existing data
    storage.clear()
    print("✓ Cleared existing data")
    
    # Create collections
    print("📁 Creating collections...")
    collection_ids = create_collections()
    print(f"✓ Created {len(collection_ids)} collections:")
    for name in collection_ids:
        print(f"  - {name}")
    print()
    
    # Create prompts
    print("📝 Creating prompts...")
    count = create_prompts(collection_ids)
    print(f"✓ Created {count} prompts")
    print()
    
    print("✅ Database seeding complete!")
    print()
    print("Sample data is ready for testing. You can now:")
    print("  1. Start the server: python main.py")
    print("  2. Visit the API docs: http://localhost:8000/docs")
    print("  3. Try creating, reading, updating, and deleting prompts!")


if __name__ == "__main__":
    main()
