from __future__ import annotations
import string
from dataclasses import dataclass, field
from enum import Enum
MIN_LENGTH = 8
BONUS_LENGTH = 12
SYMBOL_SET = string.punctuation
COMMON_PASSWORDS = {'password', 'password123', '123456', '12345678', 'qwerty', 'letmein', 'admin123', 'welcome1', 'iloveyou', 'abc12345'}

class Strength(str, Enum):
    WEAK = 'Weak'
    MEDIUM = 'Medium'
    STRONG = 'Strong'

@dataclass
class PasswordReport:
    password_length: int
    has_lower: bool
    has_upper: bool
    has_digit: bool
    has_symbol: bool
    is_common: bool
    strength: Strength
    feedback: list[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = [f'Length:        {self.password_length} characters', f'Lowercase:     {('✔' if self.has_lower else '✘')}', f'Uppercase:     {('✔' if self.has_upper else '✘')}', f'Digit:         {('✔' if self.has_digit else '✘')}', f'Symbol:        {('✔' if self.has_symbol else '✘')}', f'Common/Leaked: {('YES — avoid this password' if self.is_common else 'No')}', '-' * 40, f'Overall Strength: {self.strength.value}']
        if self.feedback:
            lines.append('Suggestions:')
            lines.extend((f'  • {tip}' for tip in self.feedback))
        return '\n'.join(lines)

def check_password_strength(password: str) -> PasswordReport:
    length = len(password)
    has_lower = any((c.islower() for c in password))
    has_upper = any((c.isupper() for c in password))
    has_digit = any((c.isdigit() for c in password))
    has_symbol = any((c in SYMBOL_SET for c in password))
    is_common = password.lower() in COMMON_PASSWORDS
    feedback: list[str] = []
    if length < MIN_LENGTH:
        feedback.append(f'Use at least {MIN_LENGTH} characters.')
        return PasswordReport(length, has_lower, has_upper, has_digit, has_symbol, is_common, Strength.WEAK, feedback)
    if is_common:
        feedback.append('This password appears in known breach lists — choose a unique one.')
        return PasswordReport(length, has_lower, has_upper, has_digit, has_symbol, is_common, Strength.WEAK, feedback)
    score = sum([has_lower, has_upper, has_digit, has_symbol])
    if length >= BONUS_LENGTH:
        score += 1
    if not has_lower:
        feedback.append('Add a lowercase letter.')
    if not has_upper:
        feedback.append('Add an uppercase letter.')
    if not has_digit:
        feedback.append('Add a number.')
    if not has_symbol:
        feedback.append('Add a symbol (e.g. !, @, #, $).')
    if length < BONUS_LENGTH:
        feedback.append(f'Consider {BONUS_LENGTH}+ characters for extra strength.')
    if score <= 2:
        strength = Strength.WEAK
    elif score in (3, 4):
        strength = Strength.MEDIUM
    else:
        strength = Strength.STRONG
        feedback.clear()
    return PasswordReport(length, has_lower, has_upper, has_digit, has_symbol, is_common, strength, feedback)

def main() -> None:
    print('=' * 44)
    print('   DecodeLabs — Password Strength Checker')
    print('=' * 44)
    try:
        password = input('\nEnter a password to evaluate: ')
    except (EOFError, KeyboardInterrupt):
        print('\nCancelled.')
        return
    if not password:
        print('No password entered. Exiting.')
        return
    report = check_password_strength(password)
    print()
    print(report.summary())
if __name__ == '__main__':
    main()