from aocd import get_data, submit
import numpy as np

data = "2333133121414131402"
data = get_data(day=9, year=2024)

def part1(input):
    disk = [int(x) for x in input]
    if len(disk) % 2 == 0:
        disk.append(0)

    fragmented_disk = []
    left_ptr = 0
    right_ptr = len(disk) - 1

    while left_ptr <= right_ptr:
        # Process file from left
        file_length = disk[left_ptr]
        file_id = left_ptr // 2
        fragmented_disk.extend([file_id] * file_length)
        left_ptr += 1

        if left_ptr > right_ptr:
            break

        # Process space and fill it with files from right
        space_length = disk[left_ptr]
        remaining_space = space_length

        while remaining_space > 0 and left_ptr <= right_ptr:
            file_length = disk[right_ptr]
            file_id = right_ptr // 2

            # Fill available space
            blocks_to_use = min(remaining_space, file_length)
            fragmented_disk.extend([file_id] * blocks_to_use)
            remaining_space -= blocks_to_use

            # Update remaining blocks for next round if any
            remaining_blocks = file_length - blocks_to_use
            if remaining_blocks > 0:
                disk[right_ptr] = remaining_blocks
            else:
                right_ptr -= 2

        left_ptr += 1

    # Calculate checksum
    checksum = 0
    for pos, val in enumerate(fragmented_disk):
        checksum += pos * val

    return checksum

def part2(input):
    disk = [int(x) for x in input]
    if len(disk) % 2 == 0:
        disk.append(0)

    # Create array to track right-side moved files
    moved_files = np.zeros((len(disk) + 1) // 2, dtype=bool)

    sorted_disk = []
    left_ptr = 0

    while left_ptr < len(disk):
        # Process file from left
        file_length = disk[left_ptr]
        file_id = left_ptr // 2

        # If file was already moved from right, add dots instead
        if moved_files[file_id]:
            sorted_disk.extend(['.'] * file_length)
        else:
            sorted_disk.extend([file_id] * file_length)
        left_ptr += 1

        if left_ptr >= len(disk):
            break

        space_length = disk[left_ptr]
        remaining_space = space_length
        right_ptr = len(disk) - 1

        while remaining_space > 0 and right_ptr > left_ptr:
            if right_ptr % 2 == 1:  # Skip spaces
                right_ptr -= 1
                continue

            file_length = disk[right_ptr]
            file_id = right_ptr // 2

            if file_length <= remaining_space and file_length > 0 and not moved_files[file_id]:
                # Found a file that fits and hasn't been moved from right yet
                sorted_disk.extend([file_id] * file_length)
                moved_files[file_id] = True
                remaining_space -= file_length

            right_ptr -= 2

        # Fill any remaining space with dots
        if remaining_space > 0:
            sorted_disk.extend(['.'] * remaining_space)

        left_ptr += 1

    checksum = 0
    for pos, val in enumerate(sorted_disk):
        if val != '.':
            checksum += pos * val

    return checksum

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")