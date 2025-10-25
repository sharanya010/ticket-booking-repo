# Ticket Booking — DevOps Assignment (Ready-to-Push)

This repository contains a minimal web-based ticket booking service and a full set of DevOps artifacts:
- Flask app (app.py)
- Dockerfile
- Jenkinsfile (CI/CD pipeline)
- Kubernetes manifests (k8s/)
- README with all commands and pipeline steps for evaluation

## Branching / Version control (GitFlow) ....
Initialize repository and follow GitFlow:
```
git init
git checkout -b develop
git checkout -b feature/your-feature
# work, commit
git add .
git commit -m "feat: add booking endpoint"
git push origin feature/your-feature
# create PR to develop, then:
git checkout develop
git merge --no-ff feature/your-feature
git checkout main
git merge --no-ff develop
git tag -a v1.0.0 -m "release v1.0.0"
git push origin --all && git push origin --tags
```

## Local build & test
Build and run locally:
```
# build
docker build -t ticket-booking:local .

# run
docker run --rm -p 5000:5000 ticket-booking:local

# smoke test
curl http://localhost:5000/
curl -X POST http://localhost:5000/book -H "Content-Type: application/json" -d '{"name":"Alice","seats":2}'
```

## Docker Hub integration
Tag and push:
```
docker tag ticket-booking:local laxmisharany6/ticket-booking:latest
docker login --username=YOUR_USER
docker push laxmisharany6/ticket-booking:latest
```

> **Jenkins pipeline** (see `Jenkinsfile`) assumes credentials stored in Jenkins:
- `dockerhub-username` and `dockerhub-password` (string credentials or username/password)
- or a credentials pair configured and referenced accordingly.
- `kubeconfig` stored in Jenkins as a secret text (the content of your kubeconfig file)

## Jenkins setup (high level)
1. Create a new Pipeline job.
2. Point it at this repository (Git URL) and set `Build when a change is pushed` (using webhooks).
3. Add Credentials:
   - Docker Hub credentials
   - Kubeconfig (as secret text)
4. Create credentials (IDs used in Jenkinsfile must match).
5. Run the pipeline — it will:
   - Checkout code
   - Build Docker image
   - Run simple smoke test
   - Push to Docker Hub
   - Deploy to Kubernetes via `kubectl apply`

## Kubernetes deployment & scaling
Apply manifests:
```
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods -l app=ticket-booking
kubectl get svc ticket-booking-service
```

Scale:
```
kubectl scale deployment ticket-booking-deployment --replicas=4
kubectl get deployment ticket-booking-deployment -o wide
```

## What to replace before pushing
1. Update `k8s/deployment.yaml` image field to your Docker Hub image (or keep as imagePullSecrets if private):
   `image: laxmisharany6/ticket-booking:TAG`
2. In `Jenkinsfile`, ensure the credential IDs match your Jenkins credentials and that `laxmisharany6/ticket-booking` env var is set in the Jenkins job (or modify the Jenkinsfile accordingly).
3. Add real screenshots of pipeline and deployments to this README for submission (place in `/docs/screenshots`).

## Files included
- app.py
- requirements.txt
- Dockerfile
- Jenkinsfile
- k8s/deployment.yaml
- k8s/service.yaml
- README.md
- .gitignore

## Notes / Evaluation checklist
- [ ] GitFlow used (feature -> develop -> main)
- [ ] Dockerfile builds a working image
- [ ] Jenkins pipeline automates build/test/push/deploy
- [ ] Kubernetes manifests deploy and scale application
- [ ] All code pushed to GitHub and link submitted

----
Good luck! If you'd like, I can also:
- Replace `laxmisharany6/ticket-booking` placeholders with your Docker Hub repo name.
- Generate a GitHub Actions pipeline instead of Jenkins.
- Create example `git` commands for creating releases or CI webhooks.
