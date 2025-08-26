# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1     | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in the Roberta Irrigator system, please report it responsibly:

### How to Report
- **Email**: Send details to the project maintainer
- **Include**: 
  - Description of the vulnerability
  - Steps to reproduce
  - Potential impact assessment
  - Suggested remediation (if known)

### What to Expect
- **Acknowledgment**: Within 48 hours of report
- **Initial Assessment**: Within 1 week
- **Resolution Timeline**: Varies based on severity (see below)
- **Credit**: Security researchers will be credited in release notes (unless anonymity is requested)

## Security Considerations

### Network Security
- **Default Ports**: Backend RPyC service on port 18871, Frontend on port 3000
- **Access Control**: No authentication implemented (local network use assumed)
- **API Endpoints**: Unprotected HTTP endpoints for zone control
- **Recommendation**: Deploy behind firewall, use VPN for remote access, under no circumstances you should expose it on internet since as for now no authentication is in place.

### Hardware Security
- **GPIO Access**: Direct hardware control requires root privileges
- **Physical Security**: Raspberry Pi should be in secure enclosure
- **Network Isolation**: Consider isolated IoT network for irrigation system

### Data Security
- **Database**: SQLite database stored locally without encryption
- **Logs**: Irrigation activity logs contain operational data
- **Backups**: No automated backup encryption implemented

## Security Best Practices

### For Deployment
1. **Network Segmentation**: Deploy on isolated IoT network
2. **Firewall Configuration**: Block external access to service ports
3. **Regular Updates**: Keep Raspberry Pi OS and dependencies updated
4. **Physical Security**: Secure hardware in weatherproof, locked enclosure
5. **Access Logging**: Monitor access to the web interface

### For Development
1. **Code Review**: All changes should be reviewed for security implications
2. **Dependency Management**: Regularly update dependencies using `./tools/repin`
3. **Input Validation**: Sanitize all user inputs in web interface
4. **Error Handling**: Avoid exposing system information in error messages

## Known Security Limitations

### Current State
- **No Authentication**: Web interface has no user authentication
- **Unencrypted Communication**: HTTP traffic not encrypted
- **Privilege Escalation**: GPIO access requires elevated privileges
- **No Rate Limiting**: API endpoints lack request rate limiting
- **Session Management**: No session security implemented

### Future Enhancements (Roadmap)
- [ ] User authentication and authorization system
- [ ] HTTPS/TLS encryption for web interface
- [ ] API rate limiting and request validation
- [ ] Database encryption at rest
- [ ] Audit logging for security events
- [ ] Role-based access control (RBAC)
- [ ] Two-factor authentication (2FA)
- [ ] Security headers and CSRF protection

## Emergency Procedures

### System Compromise
1. **Immediate**: Disconnect irrigation system from network
2. **Assessment**: Identify scope of compromise
3. **Recovery**: Restore from known good backup
4. **Analysis**: Determine attack vector and implement fixes

### Hardware Malfunction
1. **Safety First**: Emergency shutoff prevents valve damage
2. **Manual Override**: Physical valve controls should be accessible
3. **Backup Control**: Consider manual irrigation schedule backup

### Data Breach
1. **Containment**: Isolate affected systems
2. **Assessment**: Determine what data was accessed
3. **Notification**: Contact affected parties if personal data involved
4. **Remediation**: Implement fixes and monitor for further issues

## Contact Information

For security-related inquiries:
- **Project Maintainer**: Marco Chimenti
- **Response Time**: Best effort within 48 hours
- **Severity Levels**: Critical (24h), High (1 week), Medium (2 weeks), Low (next release)

## Responsible Disclosure

We request that security researchers:
- Allow reasonable time for fixes before public disclosure
- Avoid accessing or modifying user data without permission
- Report vulnerabilities privately before public discussion
- Work with us to understand and validate reported issues

Thank you for helping keep the Roberta Irrigator system secure!