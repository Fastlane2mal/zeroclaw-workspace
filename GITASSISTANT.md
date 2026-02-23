# GitAssistant Setup & Usage Guide

## Overview
This workspace is **git-backed** with automatic version control integration. All changes are tracked and synced to GitHub.

## Automatic Commits
- **Local commits**: Every 15 minutes (automatic)
- **GitHub sync**: Hourly (automatic)

Changes are continuously tracked without manual intervention required.

## Requesting Explicit Commits
To commit your work with a specific message at any time, simply ask:

> "Commit this with message: `<your message here>`"

Example:
> "Commit this with message: `feat: add user authentication`"

This allows you to create meaningful checkpoint commits between the automatic 15-minute intervals.

## GitHub Repository
**Repository URL**: https://github.com/Fastlane2mal/zeroclaw-workspace

All commits are automatically pushed to this repository during the hourly sync cycle.

## Workflow
1. Make changes in the workspace
2. Changes are automatically committed every 15 minutes
3. Commits are synced to GitHub every hour
4. Request explicit commits anytime for important milestones
