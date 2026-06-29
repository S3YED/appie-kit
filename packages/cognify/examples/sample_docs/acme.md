# Acme Robotics — engineering handbook

Acme Robotics was founded by Dana Liu and builds warehouse robots. The flagship
product, Pathfinder, is an autonomous forklift that uses ROS 2 and a LiDAR stack
for navigation.

## Team

Dana Liu leads the company. Miguel Santos owns the Pathfinder firmware and
reports to Dana. The data platform is maintained by Priya Nair, who built the
fleet telemetry pipeline on PostgreSQL and Kafka.

## Stack

Pathfinder runs on NVIDIA Jetson hardware. Telemetry is stored in PostgreSQL and
streamed through Kafka. The web dashboard is a Next.js app deployed on Vercel.
