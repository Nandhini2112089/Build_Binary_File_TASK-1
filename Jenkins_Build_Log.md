

# 📄 Jenkins Build Log Inspection Guide

This document explains how to **view build log details** and **check the size of individual Jenkins builds** from inside the Docker container.

---

##  Access Jenkins Container

```bash
docker exec -it jenkins /bin/bash
```

---

##  Navigate to a Specific Build Directory

Each Jenkins build is stored in a directory structure like:

```
/var/jenkins_home/jobs/<JOB_NAME>/builds/<BUILD_NUMBER>
```

### Example:

```bash
cd /var/jenkins_home/jobs/Password_Checker/builds/3
```

---

##  View the Build Log Output

Each build has a `log` file containing all the console output (success, errors, etc.).

```bash
cat log
```

### Sample Output:

```text
Started by user admin
Building in workspace /var/jenkins_home/workspace/Password_Checker
+ cd DOCKER_ARTIFACTORY
+ chmod +x build.sh
+ ./build.sh
Build SUCCESS
```

---

## Check the Size of a Build Folder

To know how much space a particular build is consuming:

```bash
du -sh /var/jenkins_home/jobs/Password_Checker/builds/3
```

### Example Output:

```text
4.0M    /var/jenkins_home/jobs/Password_Checker/builds/3
```

---

## Summary of Commands

| Command                                                          | Purpose                        |
| ---------------------------------------------------------------- | ------------------------------ |
| `docker exec -it jenkins /bin/bash`                              | Enter Jenkins container        |
| `cd /var/jenkins_home/jobs/<JOB_NAME>/builds/<BUILD_NUMBER>`     | Go to specific build directory |
| `cat log`                                                        | View build output              |
| `du -sh /var/jenkins_home/jobs/<JOB_NAME>/builds/<BUILD_NUMBER>` | Check size of a build          |

---

