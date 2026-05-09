# Profiling Hard Drive

You can use the **df** and **du** commands to get a clear profile of your hard drive and see how much local space is being used, including by folders used for remote drives like Dropbox and Google Drive (which typically have local sync folders).

**Summary of recommended commands:**

- To get an _overview_ of total space used per mounted filesystem (including core local and synced cloud folders):

  ```
  df -H --output=source,target,size,used,avail
  ```

  This shows local disks and any separate mounts (network or removable), with space used, available, and where they’re mounted[1][2][4].

- To _profile local storage_ per folder (helpful for cloud storage folders that only partially sync locally):

  ```
  du -sh ~/*
  ```

  Replace `~/*` with paths like `~/Dropbox`, `~/Google Drive`, or wherever your cloud clients keep their files to see how much space their local cache or selectively-synced data is using[1][2][4].

- To _see top space-consuming subfolders_ (find heavy usage quickly):

  ```
  du -h ~/ | sort -hr | head -n 20
  ```

  This lets you rapidly identify space hogs, including cloud sync folders, which may be selectively mirrored[1][4].

**Notes and key points:**

- Sync clients like Dropbox, Google Drive, and OneDrive typically store local copies in default locations (e.g., `~/Dropbox`, `~/Google Drive`).
- These commands only show **local disk usage**—not the cloud storage that’s online-only.
- To _distinguish_ between remote-mounted file systems (e.g., network drives) and local folders synced from the cloud, look at the "source" and "target" columns in the `df` output.
- For a more interactive/visual report, tools like **ncdu** (Linux/macOS, not always preinstalled) or **gdu** (Linux) can help navigate space usage fast from the command line[3][4].

**Example for both core and cloud (replace folder names as needed):**

```bash
echo "Summary of total disk usage:"
df -H --output=source,target,size,used,avail

echo "Local space used by cloud folders:"
du -sh ~/Dropbox ~/Google\ Drive ~/OneDrive 2>/dev/null
```

These approaches give you both a **breakdown of space by filesystem** and a **summary of space consumed locally by synced cloud storage**[1][2][4].
