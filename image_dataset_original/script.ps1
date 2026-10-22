# Set the base directory
$baseDir = "C:\Users\jfpal\OneDrive - University of the West of Scotland\Final project\Final_Version\RPi\IoT_project\image_dataset"

# Get all subdirectories in the base directory
$subDirs = Get-ChildItem -Path $baseDir -Directory

foreach ($subDir in $subDirs) {
    # Get the inner directory
    $innerDirs = Get-ChildItem -Path $subDir.FullName -Directory

    if ($innerDirs.Count -eq 1) {
        $innerDir = $innerDirs[0]

        # Move all files from the inner directory to the outer directory
        Get-ChildItem -Path $innerDir.FullName | Move-Item -Destination $subDir.FullName

        # Remove the now-empty inner directory
        Remove-Item -Path $innerDir.FullName -Recurse -Force
    }
}

Write-Output "Done."
