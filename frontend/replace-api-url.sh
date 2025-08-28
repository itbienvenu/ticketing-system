#!/bin/bash

# Hardcoded URL to replace
OLD_URL="http://127.0.0.1:8000/api/v1"

# Target folder
TARGET_DIR="./src"

# Backup first
echo "Backing up JS and Vue files..."
mkdir -p backup_code
find "$TARGET_DIR" -type f \( -name "*.js" -o -name "*.vue" \) -exec cp {} backup_code/ \;

# Loop over files safely
echo "Processing files..."
find "$TARGET_DIR" -type f \( -name "*.js" -o -name "*.vue" \) | while IFS= read -r file; do
  echo "Processing $file ..."

  # Add API_BASE definition at top if not exists
  if ! grep -q "const API_BASE" "$file"; then
    # Insert at first line
    sed -i "1i const API_BASE = process.env.VUE_APP_API_BASE_URL;" "$file"
  fi

  # Replace old URLs with ${API_BASE}
  sed -i "s|\"$OLD_URL\"|\`\${API_BASE}\`|g" "$file"
  sed -i "s|'$OLD_URL'|\`\${API_BASE}\`|g" "$file"
done

echo "Replacement done! Old files are backed up in backup_code/"
