from aocd import get_data, submit

data = "1\n10\n100\n2024"  # Example data from puzzle
# data = get_data(day=22, year=2024)

def update_secret(secret):
    # Step 1: multiply by 64, mix (XOR), and prune
    result = secret * 64
    secret = secret ^ result
    secret = secret % 16777216

    # Step 2: divide by 32 (floor division), mix, and prune
    result = secret // 32
    secret = secret ^ result
    secret = secret % 16777216

    # Step 3: multiply by 2048, mix, and prune
    result = secret * 2048
    secret = secret ^ result
    secret = secret % 16777216

    return secret

def part1(secrets):
    result = 0
    for initial_secret in secrets:
        secret = initial_secret
        for _ in range(2000):
            secret = update_secret(secret)
        result += secret
    return result

def part2(secrets):
    all_sequences = {}

    for initial_secret in secrets:
        prices = [initial_secret % 10]
        secret = initial_secret

        seen_sequences = set()


        for _ in range(2000):
            secret = update_secret(secret)
            prices.append(secret % 10)

            # Only proceed if we have enough prices for a sequence
            if len(prices) >= 5:
                changes = []
                for i in range(len(prices)-5, len(prices)-1):
                    changes.append(prices[i+1] - prices[i])

                sequence = tuple(changes)

                if sequence not in seen_sequences:
                    seen_sequences.add(sequence)

                    if sequence in all_sequences:
                        all_sequences[sequence] = all_sequences[sequence] + [prices[-1]]
                    else:
                        all_sequences[sequence] = [prices[-1]]

                prices.pop(0)

    max_bananas = 0
    best_sequence = None
    for sequence, bananas in all_sequences.items():
        if sum(bananas) > max_bananas:
            max_bananas = sum(bananas)
            best_sequence = sequence

    print(f"Best sequence: {best_sequence}")
    return max_bananas

secrets = [int(x) for x in data.splitlines()]
print(f"Part 1: {part1(secrets)}")
print(f"Part 2: {part2(secrets)}")