from bs4 import BeautifulSoup
import os
import bs4
formatter = bs4.formatter.HTMLFormatter(indent=4)

def update_structure(template_path, target_files):
    # Load the template HTML
    with open(template_path, "r") as f:
        template = f.read()
    template_soup = BeautifulSoup(template, "html.parser")

    # Iterate through each target file
    for file_path in target_files:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        
        # Load the target file
        with open(file_path, "r") as f:
            target_content = f.read()
        target_soup = BeautifulSoup(target_content, "html.parser")
        
        # Extract the content inside id="content"
        content_div = target_soup.find(id="content")
        if not content_div:
            print(f"No content section found in: {file_path}")
            continue
        
        # Save the dynamic content temporarily
        dynamic_content = content_div.decode_contents()

        # Update the target file with the template structure
        new_content_div = template_soup.find(id="content")
        if not new_content_div:
            print(f"No content section found in the template: {template_path}")
            continue
        
        # Insert the saved content into the new structure
        new_content_div.clear()  # Clear the placeholder content in the template
        new_content_div.append(BeautifulSoup(dynamic_content, "html.parser"))
        
        # Save the updated file
        with open(file_path, "w") as f:
            f.write(str(template_soup.prettify(formatter=formatter)))
        print(f"File updated successfully: {file_path}")

# Example usage
# template_file = "admin_view_template.html"
# target_files = [
#     "admin_dashboard.html", 
#     "admin_community.html", 
#     "admin_content.html",
#     "admin_analytics.html",
#     "admin_copyright.html",
#     "admin_earn.html",
#     ]

# template_file = "content_dashboard_template.html"
# target_files = [
#     'content_analytics.html',
#     'content_comments.html',
#     'content_copyright.html',
#     'content_details.html',
#     'content_editor.html',
#     'content_translate.html',

# ]
template_file = "user_view_template.html"
target_files = [
    'index.html',
    'book_view.html',
    'profile.html'
]
update_structure(template_file, target_files)
