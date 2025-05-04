playbooks = {
    'malware': [
        "Step 1: Isolate the infected system from the network.",
        "Step 2: Run an antivirus/anti-malware scan to identify malicious files.",
        "Step 3: Quarantine any suspicious files identified by the scanner.",
        "Step 4: Analyze the malware using a sandbox or reverse engineering tools.",
        "Step 5: Report findings to the security operations team."
    ],
    'phishing': [
        "Step 1: Identify the phishing email sender and assess the damage.",
        "Step 2: Block the sender’s domain and any linked URLs in the email.",
        "Step 3: Alert other users to be cautious of similar phishing emails.",
        "Step 4: Check if any sensitive information was accessed or leaked.",
        "Step 5: Investigate the phishing attack's vector (email, social media, etc.)."
    ],
    'ransomware': [
        "Step 1: Isolate all affected systems from the network immediately.",
        "Step 2: Identify the ransom note and analyze any files encrypted.",
        "Step 3: Report the attack to relevant authorities, if applicable.",
        "Step 4: Attempt decryption using known methods or recovery keys.",
        "Step 5: Restore from backups and strengthen network security to prevent future attacks."
    ],
    # Additional alert types (DDoS, SQL Injection, etc.) can be added here
}
