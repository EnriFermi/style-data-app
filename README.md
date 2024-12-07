
---

# Program Startup Guide

## Setup Instructions

1. **Prepare Stylizations Directory**  
   - Create a directory named `stylizations` in the same location as the program.  
   - Add all the required images to this directory.  

   **Important:**  
   - Stylized images should follow the naming convention:  
     `content_<content_id>_...`  
     This naming is crucial for the shuffling process to work correctly.

2. **Run the Program**  
   Execute the following command:  
   ```
   python app.py
   ```

## Directory Structure

Upon execution, the program will automatically create the following directories in the launch location:  
- **`output/`**: Contains user responses saved as CSV files.  
- **`index_file/`**: Stores the order in which shuffled files are presented to the user.  

### Nested Directories  
If the `stylizations` directory contains subdirectories, the program will recursively collect all `.jpg` files.

## Command-Line Parameters

The program supports the following optional parameters:  

| Parameter         | Description                                         | Default Value          |
|--------------------|-----------------------------------------------------|------------------------|
| `--data`     | Name of the stylizations directory.                 | `stylizations`         |
| `--out`       | Name of the output scores directory.                | `output`               |
| `--index`   | Name of the shuffling index directory.              | `index_file`           |

Example usage:  
```
python app.py --data my_stylizations --out results --index shuffle_index
```

--- 

This is pure raw text, formatted as Markdown, without any additional styling added by editors.