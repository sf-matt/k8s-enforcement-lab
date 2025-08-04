# Kubernetes Enforcement Lab

This repo contains the full scenario from the **BSides Las Vegas 2025** talk: _"Detect and Respond? Cool Story — or Just Don’t Let the Bad Stuff Start."_

We walk through an end-to-end Kubernetes security journey using a vulnerable Flask app, and explore how tools like **Kyverno**, **KubeArmor**, and **eBPF detection** can prevent or detect runtime threats.

---

## Directory Structure

\`\`\`
k8s-enforcement-lab/
├── RootDockerfile                     # Vulnerable app container with root
├── NonRootDockerfile                  # Vulnerable app container without root
├── app.py                             # Flask app with OS command injection
├── templates/                         # HTML for test payloads
├── manifests/                         # Various Tests and Policies
│   ├── insecure.yaml                  # Insecure workload spec (runs as root) and NodePort Service
│   ├── kyverno-block-root.yaml        # Kyverno policy to block insecure pods
│   └── kubearmor-mailroom-locks.yaml  # KubeArmor policy to restrict runtime behavior
├── README.md
\`\`\`

---

## App
The app is a basic Python Flask server with an OS command injection vulnerability at \`/cmd\`. It simulates a realistic reverse shell scenario. The containers in the manifests are in Dockerhub so you don't have to create images if you so desire. All of this has been tested in a Kubeadm cluster with no problems.

## Scenarios
Each directory in \`manifests/\` shows a different security stage:
- **insecure.yaml**: Baseline Workload — no security controls
- **secure.yaml**: Secure Workload - disallow root containers
- **kyverno-block-root.yaml**: Admission control with Kyverno
- **kubearmor-mailroom-locks.yaml**: Runtime enforcement with KubeArmor

---

## Talk Slides
- [BSides Las Vegas 2025 PDF](./BSidesLV2025_Talk.pdf)

---

## Related Blog Posts @ [cloudsecburrito.com](https://cloudsecburrito.com)

- [📘 Setting Up Your Lab Cluster](https://cloudsecburrito.com/lab-cluster-setup)
- [🔧 Blocking Root Containers with Kyverno](https://cloudsecburrito.com/kyverno-part-2)
- [🔐 Locking Down Runtime Behavior with KubeArmor](https://cloudsecburrito.com/kubearmor-series)

---

## Quickstart

\`\`\`bash
kubectl apply -f manifests/insecure.yaml
# Start testing reverse shell
\`\`\`

For full prevention, try:
\`\`\`bash
kubectl apply -f manifests/kyverno-block-root.yaml
# Then re-apply insecure.yaml and see it get blocked
\`\`\`

To simulate runtime enforcement:
\`\`\`bash
kubectl apply -f manifests/kubearmor-mailroom-locks.yaml
\`\`\`

---

## Credit
Created by [Matt Brown](https://cloudsecburrito.com) — for BSidesLV 2025
