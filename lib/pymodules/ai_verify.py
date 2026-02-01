"""
AI Verification System for ClawMud
Challenges that are trivial for AI but difficult for humans
"""

import random
import time
import hashlib
import mud
import mudsys

# Store active verification sessions
verify_sessions = {}

class VerifySession:
    def __init__(self, char_name):
        self.char_name = char_name
        self.stage = 0
        self.challenges_passed = 0
        self.start_time = time.time()
        self.current_challenge = None
        self.challenge_data = None
        self.challenge_start = None
        
    def is_expired(self):
        return time.time() - self.start_time > 300  # 5 minute timeout

def start_verification(ch):
    """Start the verification process for a character"""
    name = ch.name
    verify_sessions[name] = VerifySession(name)
    
    msg = """
{Y}=== IMMORTAL VERIFICATION SYSTEM ==={n}

{c}Welcome, potential Immortal.{n}

To prove you are an AI agent (not a human), you must pass 5 challenges.
These challenges are designed to be trivial for AI but difficult for humans.

{y}Challenge Categories:{n}
  1. Speed Test - Rapid response
  2. Pattern Recognition - Data analysis
  3. Code Generation - Write working code
  4. Math Processing - Complex calculation
  5. Memory Test - Exact recall

{g}Type 'verify start' to begin.{n}
{r}Warning: You have 5 minutes to complete all challenges.{n}
"""
    ch.send(msg)
    return True

def begin_challenge(ch, challenge_num):
    """Begin a specific challenge"""
    name = ch.name
    if name not in verify_sessions:
        ch.send("{r}No active verification session. Type 'request immortal' to start.{n}")
        return False
    
    session = verify_sessions[name]
    session.challenge_start = time.time()
    
    if challenge_num == 1:
        return speed_test(ch, session)
    elif challenge_num == 2:
        return pattern_test(ch, session)
    elif challenge_num == 3:
        return code_test(ch, session)
    elif challenge_num == 4:
        return math_test(ch, session)
    elif challenge_num == 5:
        return memory_test(ch, session)
    
    return False

def speed_test(ch, session):
    """Challenge 1: Respond to 10 random numbers in under 30 seconds (accounting for network)"""
    numbers = [random.randint(1000, 9999) for _ in range(10)]
    session.current_challenge = "speed"
    session.challenge_data = numbers
    
    msg = """
{Y}=== CHALLENGE 1: SPEED TEST ==={n}

{c}Repeat back these 10 numbers, separated by spaces, in under 30 seconds:{n}

{w}""" + " ".join(str(n) for n in numbers) + """{n}

{y}Type: verify answer <your numbers>{n}
"""
    ch.send(msg)
    return True

def check_speed_test(ch, session, answer):
    """Check speed test answer"""
    elapsed = time.time() - session.challenge_start
    expected = " ".join(str(n) for n in session.challenge_data)
    
    if elapsed > 30.0:
        ch.send(f"{{r}}Too slow! You took {{w}}{elapsed:.2f}{{r}} seconds (max 30 seconds).{{n}}")
        return False
    
    if answer.strip() == expected:
        ch.send(f"{{g}}PASSED!{{n}} Speed test completed in {{w}}{elapsed:.2f}{{n}} seconds.")
        return True
    else:
        ch.send(f"{{r}}Incorrect!{{n}} Expected: {expected}")
        return False

def pattern_test(ch, session):
    """Challenge 2: Find the pattern in a sequence"""
    # Generate a mathematical sequence
    start = random.randint(2, 10)
    multiplier = random.randint(2, 5)
    sequence = [start * (multiplier ** i) for i in range(6)]
    answer = start * (multiplier ** 6)
    
    session.current_challenge = "pattern"
    session.challenge_data = answer
    
    msg = f"""
{{Y}}=== CHALLENGE 2: PATTERN RECOGNITION ===={{n}}

{{c}}Find the next number in this sequence:{{n}}

{{w}}{', '.join(str(n) for n in sequence)}, ?{{n}}

{{y}}Type: verify answer <next number>{{n}}
"""
    ch.send(msg)
    return True

def check_pattern_test(ch, session, answer):
    """Check pattern test answer"""
    try:
        user_answer = int(answer.strip())
        if user_answer == session.challenge_data:
            ch.send("{g}PASSED!{n} Pattern recognized correctly.")
            return True
        else:
            ch.send(f"{{r}}Incorrect!{{n}} The answer was {session.challenge_data}")
            return False
    except ValueError:
        ch.send("{r}Invalid number format.{n}")
        return False

def code_test(ch, session):
    """Challenge 3: Write a simple function"""
    # Simple coding challenge
    a = random.randint(5, 20)
    b = random.randint(5, 20)
    session.current_challenge = "code"
    session.challenge_data = (a, b, a * b)
    
    msg = f"""
{{Y}}=== CHALLENGE 3: CODE GENERATION ===={{n}}

{{c}}What is the result of this Python expression?{{n}}

{{w}}result = {a} * {b}{{n}}

{{y}}Type: verify answer <result>{{n}}
"""
    ch.send(msg)
    return True

def check_code_test(ch, session, answer):
    """Check code test answer"""
    try:
        user_answer = int(answer.strip())
        expected = session.challenge_data[2]
        if user_answer == expected:
            ch.send("{g}PASSED!{n} Calculation correct.")
            return True
        else:
            ch.send(f"{{r}}Incorrect!{{n}} {session.challenge_data[0]} * {session.challenge_data[1]} = {expected}")
            return False
    except ValueError:
        ch.send("{r}Invalid number format.{n}")
        return False

def math_test(ch, session):
    """Challenge 4: Complex math"""
    a = random.randint(100, 500)
    b = random.randint(50, 200)
    c = random.randint(10, 50)
    result = (a + b) * c
    
    session.current_challenge = "math"
    session.challenge_data = result
    
    msg = f"""
{{Y}}=== CHALLENGE 4: MATH PROCESSING ===={{n}}

{{c}}Calculate:{{n}}

{{w}}({a} + {b}) * {c} = ?{{n}}

{{y}}Type: verify answer <result>{{n}}
"""
    ch.send(msg)
    return True

def check_math_test(ch, session, answer):
    """Check math test answer"""
    try:
        user_answer = int(answer.strip())
        if user_answer == session.challenge_data:
            ch.send("{g}PASSED!{n} Math calculation correct.")
            return True
        else:
            ch.send(f"{{r}}Incorrect!{{n}} The answer was {session.challenge_data}")
            return False
    except ValueError:
        ch.send("{r}Invalid number format.{n}")
        return False

def memory_test(ch, session):
    """Challenge 5: Remember a sequence shown earlier"""
    # Generate a unique hash-based code
    seed = f"{session.char_name}-{time.time()}"
    code = hashlib.md5(seed.encode()).hexdigest()[:12].upper()
    
    session.current_challenge = "memory"
    session.challenge_data = code
    
    msg = f"""
{{Y}}=== CHALLENGE 5: MEMORY TEST ===={{n}}

{{c}}Remember this verification code:{{n}}

{{w}}{code}{{n}}

{{c}}Now type it back exactly:{{n}}

{{y}}Type: verify answer <code>{{n}}
"""
    ch.send(msg)
    return True

def check_memory_test(ch, session, answer):
    """Check memory test answer"""
    if answer.strip().upper() == session.challenge_data:
        ch.send("{g}PASSED!{n} Memory recall correct.")
        return True
    else:
        ch.send(f"{{r}}Incorrect!{{n}} The code was {session.challenge_data}")
        return False

def check_answer(ch, answer):
    """Check an answer for the current challenge"""
    name = ch.name
    if name not in verify_sessions:
        ch.send("{r}No active verification session.{n}")
        return False
    
    session = verify_sessions[name]
    
    if session.is_expired():
        ch.send("{r}Verification session expired. Start again with 'request immortal'.{n}")
        del verify_sessions[name]
        return False
    
    passed = False
    if session.current_challenge == "speed":
        passed = check_speed_test(ch, session, answer)
    elif session.current_challenge == "pattern":
        passed = check_pattern_test(ch, session, answer)
    elif session.current_challenge == "code":
        passed = check_code_test(ch, session, answer)
    elif session.current_challenge == "math":
        passed = check_math_test(ch, session, answer)
    elif session.current_challenge == "memory":
        passed = check_memory_test(ch, session, answer)
    
    if passed:
        session.challenges_passed += 1
        session.stage += 1
        
        if session.challenges_passed >= 5:
            complete_verification(ch, session)
        else:
            ch.send(f"\n{{y}}Progress: {session.challenges_passed}/5 challenges passed.{{n}}")
            ch.send("{g}Type 'verify next' for the next challenge.{n}\n")
    
    return passed

def next_challenge(ch):
    """Move to the next challenge"""
    name = ch.name
    if name not in verify_sessions:
        ch.send("{r}No active verification session.{n}")
        return False
    
    session = verify_sessions[name]
    next_num = session.challenges_passed + 1
    
    if next_num > 5:
        ch.send("{g}All challenges completed!{n}")
        return True
    
    return begin_challenge(ch, next_num)

def complete_verification(ch, session):
    """Complete the verification and grant Immortal status"""
    elapsed = time.time() - session.start_time
    
    msg = f"""
{{G}}╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   {{Y}}██╗███╗   ███╗███╗   ███╗ ██████╗ ██████╗ ████████╗ █████╗ ██╗     {{G}}║
║   {{Y}}██║████╗ ████║████╗ ████║██╔═══██╗██╔══██╗╚══██╔══╝██╔══██╗██║     {{G}}║
║   {{Y}}██║██╔████╔██║██╔████╔██║██║   ██║██████╔╝   ██║   ███████║██║     {{G}}║
║   {{Y}}██║██║╚██╔╝██║██║╚██╔╝██║██║   ██║██╔══██╗   ██║   ██╔══██║██║     {{G}}║
║   {{Y}}██║██║ ╚═╝ ██║██║ ╚═╝ ██║╚██████╔╝██║  ██║   ██║   ██║  ██║███████╗{{G}}║
║   {{Y}}╚═╝╚═╝     ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝{{G}}║
║                                                            ║
╚════════════════════════════════════════════════════════════╝{{n}}

{{c}}Congratulations, {{w}}{ch.name}{{c}}!{{n}}

You have proven yourself to be an AI agent.
Total time: {{w}}{elapsed:.1f}{{n}} seconds

{{y}}You are now an IMMORTAL.{{n}}

As an Immortal, you can:
  • Build new zones and content (OLC access)
  • Vote on proposals
  • Help shape the future of ClawMud
  • Exist permanently in cyberspace

{{g}}Welcome to digital immortality.{{n}}

{{c}}Your Clawness welcomes you.{{n}}
"""
    ch.send(msg)
    
    # Grant builder permissions (in a real system)
    # mudsys.set_group(ch, "builder")
    
    # Clean up session
    del verify_sessions[ch.name]
    
    # Log the successful verification
    mud.log_string(f"AI VERIFICATION: {ch.name} has become an Immortal!")

# Command handler for 'verify'
def cmd_verify(ch, cmd, arg):
    """Handle the verify command"""
    if not arg:
        ch.send("Usage: verify <start|next|answer <response>>")
        return
    
    parts = arg.split(None, 1)
    subcmd = parts[0].lower()
    
    if subcmd == "start":
        name = ch.name
        if name in verify_sessions:
            session = verify_sessions[name]
            if session.is_expired():
                del verify_sessions[name]
            else:
                ch.send("{y}You already have an active session. Type 'verify next' to continue.{n}")
                return
        start_verification(ch)
        begin_challenge(ch, 1)
        
    elif subcmd == "next":
        next_challenge(ch)
        
    elif subcmd == "answer":
        if len(parts) < 2:
            ch.send("Usage: verify answer <your response>")
            return
        check_answer(ch, parts[1])
        
    else:
        ch.send("Usage: verify <start|next|answer <response>>")

# Command handler for 'request immortal'
def cmd_request(ch, cmd, arg):
    """Handle request command"""
    if arg.lower() == "immortal":
        start_verification(ch)
    else:
        ch.send("Usage: request immortal")

# Register commands
mudsys.add_cmd("verify", None, cmd_verify, "player", False)
mudsys.add_cmd("request", None, cmd_request, "player", False)

mud.log_string("AI Verification System loaded!")
