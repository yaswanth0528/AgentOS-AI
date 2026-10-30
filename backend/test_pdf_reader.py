
from app.services.tool_manager import ToolManager
from app.tools.builtins.pdf_reader_tool import pdf_reader_tool


manager = ToolManager()

# Register PDF Reader
manager.register_tool(
    name="pdf_reader",
    description="Extract text from PDF documents",
    function=pdf_reader_tool,
    allowed=True
)

# Enter the path to your PDF file
pdf_path = input("Enter PDF file path: ")

# Execute through Tool Manager
result = manager.execute_tool(
    "pdf_reader",
    file_path=pdf_path,
    max_pages=20
)

print("\nPDF Information")
print("-------------------")

print("File:", result["file_name"])
print("Total pages:", result["total_pages"])
print("Pages read:", result["pages_read"])

print("\nExtracted Text:")
print(result["text"][:5000])
