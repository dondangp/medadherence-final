# =================================================================================================
# Medication Administration Record Generator
# 
# This script generates medication administration records for different time periods
# with options for today only, last week, current month, or past 90 days.
# It prevents duplicates by checking existing records before creating new ones.
# =================================================================================================

# Configure command line options for different time periods and output settings

# Medicine definitions - each medication has information needed to create administration records

# Helper function to determine date range based on the selected time period option

# Load existing medication records to prevent duplicates
# Creates a unique key for each medication-date combination

# Generate dates with a realistic distribution pattern
# Different patterns for short timeframes vs longer periods

# Calculate number of records to create based on medication frequency and time period
# Daily medications taken most days, as-needed medications taken occasionally

# Duplicate prevention - check if a record already exists for this medication on this date
# Skip creating records when duplicates found, and generate extra dates to compensate

# Write all records to file, sorting by date
# Either replace existing file or append to it based on options

# Display statistics about created records, duplicates skipped, and file information

import json
import uuid
from datetime import datetime, timedelta, date
import random
import os
import argparse

# Setup command line arguments
parser = argparse.ArgumentParser(description='Generate medication administration records for specific time periods.')
group = parser.add_mutually_exclusive_group()
group.add_argument('--today', action='store_true', help='Generate records for today only')
group.add_argument('--week', action='store_true', help='Generate records for the last 7 days')
group.add_argument('--month', action='store_true', help='Generate records for the current month')
group.add_argument('--all', action='store_true', help='Generate records for the past 90 days (default)')
parser.add_argument('--output', default="fhir_data/medication_administration/MedicationAdministration.ndjson", 
                   help='Output file path')
parser.add_argument('--append', action='store_true', help='Append to existing file instead of overwriting')

args = parser.parse_args()

# Define the path to your medication administration file
med_admin_path = args.output

# Sample medication data in the format your application uses
medications = [
    {
        "Medication": "Astemizole 10 MG Oral Tablet",
        "RXnormCode": "197378",
        "RXnormSystem": "http://www.nlm.nih.gov/research/umls/rxnorm",
        "RXnormDisplay": "Astemizole 10 MG Oral Tablet",
        "Original": {
            "subject": {"reference": "Patient/42ed5c35-3c36-136a-1179-7af73df61d8c"},
            "encounter": {"reference": "Encounter/2be97abd-2ed1-e59f-c39c-f195662800ed"},
            "reasonCode": [
                {
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/reason-medication-given",
                        "code": "b",
                        "display": "Given as Ordered"
                    }],
                    "text": "Self-administered medication"
                }
            ]
        }
    },
    {
        "Medication": "Hydrocortisone 10 MG/ML Topical Cream",
        "RXnormCode": "106258",
        "RXnormSystem": "http://www.nlm.nih.gov/research/umls/rxnorm",
        "RXnormDisplay": "Hydrocortisone 10 MG/ML Topical Cream",
        "Original": {
            "subject": {"reference": "Patient/42ed5c35-3c36-136a-1179-7af73df61d8c"},
            "encounter": {"reference": "Encounter/75122b18-647b-59e0-d23f-d1d8e41fa2e6"},
            "reasonCode": [
                {
                    "coding": [{
                        "system": "http://snomed.info/sct",
                        "code": "40275004",
                        "display": "Contact dermatitis (disorder)"
                    }],
                    "text": "Contact dermatitis (disorder)"
                }
            ]
        }
    },
    {
        "Medication": "Simvastatin 20 MG Oral Tablet",
        "RXnormCode": "312961",
        "RXnormSystem": "http://www.nlm.nih.gov/research/umls/rxnorm",
        "RXnormDisplay": "Simvastatin 20 MG Oral Tablet",
        "Original": {
            "subject": {"reference": "Patient/42ed5c35-3c36-136a-1179-7af73df61d8c"},
            "encounter": {"reference": "Encounter/afadb6b9-023f-7b75-0713-dcef89186756"},
            "reasonCode": [
                {
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/reason-medication-given",
                        "code": "b",
                        "display": "Given as Ordered"
                    }],
                    "text": "Self-administered medication"
                }
            ]
        }
    },
    {
        "Medication": "24 HR metoprolol succinate 100 MG Extended Release Oral Tablet",
        "RXnormCode": "866412",
        "RXnormSystem": "http://www.nlm.nih.gov/research/umls/rxnorm",
        "RXnormDisplay": "24 HR metoprolol succinate 100 MG Extended Release Oral Tablet",
        "Original": {
            "subject": {"reference": "Patient/42ed5c35-3c36-136a-1179-7af73df61d8c"},
            "encounter": {"reference": "Encounter/afadb6b9-023f-7b75-0713-dcef89186756"},
            "reasonCode": [
                {
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/reason-medication-given",
                        "code": "b",
                        "display": "Given as Ordered"
                    }],
                    "text": "Self-administered medication"
                }
            ]
        }
    },
    {
        "Medication": "Clopidogrel 75 MG Oral Tablet",
        "RXnormCode": "309362",
        "RXnormSystem": "http://www.nlm.nih.gov/research/umls/rxnorm",
        "RXnormDisplay": "Clopidogrel 75 MG Oral Tablet",
        "Original": {
            "subject": {"reference": "Patient/42ed5c35-3c36-136a-1179-7af73df61d8c"},
            "encounter": {"reference": "Encounter/afadb6b9-023f-7b75-0713-dcef89186756"},
            "reasonCode": [
                {
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/reason-medication-given",
                        "code": "b",
                        "display": "Given as Ordered"
                    }],
                    "text": "Self-administered medication"
                }
            ]
        }
    },
    {
        "Medication": "Nitroglycerin 0.4 MG/ACTUAT Mucosal Spray",
        "RXnormCode": "705129",
        "RXnormSystem": "http://www.nlm.nih.gov/research/umls/rxnorm",
        "RXnormDisplay": "Nitroglycerin 0.4 MG/ACTUAT Mucosal Spray",
        "Original": {
            "subject": {"reference": "Patient/42ed5c35-3c36-136a-1179-7af73df61d8c"},
            "encounter": {"reference": "Encounter/afadb6b9-023f-7b75-0713-dcef89186756"},
            "reasonCode": [
                {
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/reason-medication-given",
                        "code": "b",
                        "display": "Given as Ordered"
                    }],
                    "text": "Self-administered medication"
                }
            ]
        }
    },
    {
        "Medication": "Acetaminophen 300 MG / Hydrocodone Bitartrate 5 MG Oral Tablet",
        "RXnormCode": "856987",
        "RXnormSystem": "http://www.nlm.nih.gov/research/umls/rxnorm",
        "RXnormDisplay": "Acetaminophen 300 MG / Hydrocodone Bitartrate 5 MG Oral Tablet",
        "Original": {
            "subject": {"reference": "Patient/42ed5c35-3c36-136a-1179-7af73df61d8c"},
            "encounter": {"reference": "Encounter/753fde06-26d8-c869-f55d-1f918904720a"},
            "reasonCode": [
                {
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/reason-medication-given",
                        "code": "b",
                        "display": "Given as Ordered"
                    }],
                    "text": "Self-administered medication"
                }
            ]
        }
    }
]

def get_date_range():
    """Determine the date range based on command line arguments"""
    today = datetime.now()
    
    if args.today:
        # Today only
        start_date = today
        end_date = today
        print(f"Generating records for today: {today.strftime('%Y-%m-%d')}")
    elif args.week:
        # Last 7 days
        start_date = today - timedelta(days=6)  # 7 days including today
        end_date = today
        print(f"Generating records for the last 7 days: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    elif args.month:
        # Current month
        start_date = today.replace(day=1)  # First day of current month
        end_date = today
        print(f"Generating records for the current month: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    else:
        # Default: 90 days
        start_date = today - timedelta(days=89)  # 90 days including today
        end_date = today
        print(f"Generating records for the past 90 days: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    return start_date, end_date

# Read existing records to avoid duplicates
def load_existing_records():
    """Load existing medication administration records"""
    existing_records = []
    # Key format: "med_code:date"
    existing_med_dates = set()
    
    if os.path.exists(med_admin_path) and args.append:
        try:
            with open(med_admin_path, 'r') as f:
                for line in f:
                    if line.strip():
                        record = json.loads(line)
                        existing_records.append(record)
                        
                        # Extract medication code
                        med_code = None
                        for coding in record.get("medicationCodeableConcept", {}).get("coding", []):
                            if coding.get("system") == "http://www.nlm.nih.gov/research/umls/rxnorm":
                                med_code = coding.get("code")
                                break
                        
                        # Extract date (just the date part, not time)
                        try:
                            date_str = record.get("effectiveDateTime", "").split('T')[0]
                        except:
                            date_str = ""
                        
                        if med_code and date_str:
                            existing_med_dates.add(f"{med_code}:{date_str}")
            
            print(f"Loaded {len(existing_records)} existing records")
            print(f"Found {len(existing_med_dates)} unique medication-date combinations")
        except Exception as e:
            print(f"Error loading existing records: {e}")
    
    return existing_records, existing_med_dates

# Generate dates distributed within the specified time period
def generate_dates(start_date, end_date, total_entries=20):
    """Generate dates within the specified range with more entries for recent dates"""
    if start_date == end_date:
        # If only generating for today, create entries with different times
        times = []
        for _ in range(total_entries):
            # Random time between 6am and 10pm
            hour = random.randint(6, 22)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            times.append(datetime.now().replace(hour=hour, minute=minute, second=second))
        return times
    
    # Create more entries for recent dates when range spans multiple days
    dates = []
    days_in_range = (end_date - start_date).days + 1
    
    # If time span is a week or less, distribute more evenly
    if days_in_range <= 7:
        # More even distribution for shorter time periods
        for _ in range(total_entries):
            days_ago = random.randint(0, days_in_range - 1)
            date = end_date - timedelta(days=days_ago)
            # Add random time
            hour = random.randint(6, 22)
            minute = random.randint(0, 59)
            date = date.replace(hour=hour, minute=minute, second=0)
            dates.append(date)
    else:
        # Last third of the period - 60% of entries (more recent)
        recent_period = max(days_in_range // 3, 1)
        for _ in range(int(total_entries * 0.6)):
            days_ago = random.randint(0, recent_period)
            date = end_date - timedelta(days=days_ago)
            # Add random time
            hour = random.randint(6, 22)
            minute = random.randint(0, 59)
            date = date.replace(hour=hour, minute=minute, second=0)
            dates.append(date)
        
        # Middle third of the period - 30% of entries
        for _ in range(int(total_entries * 0.3)):
            days_ago = random.randint(recent_period + 1, 2 * recent_period)
            date = end_date - timedelta(days=days_ago)
            # Add random time
            hour = random.randint(6, 22)
            minute = random.randint(0, 59)
            date = date.replace(hour=hour, minute=minute, second=0)
            dates.append(date)
        
        # First third of the period - 10% of entries (oldest)
        for _ in range(int(total_entries * 0.1)):
            days_ago = random.randint(2 * recent_period + 1, days_in_range - 1)
            if days_ago >= days_in_range:
                days_ago = days_in_range - 1
            date = end_date - timedelta(days=days_ago)
            # Add random time
            hour = random.randint(6, 22)
            minute = random.randint(0, 59)
            date = date.replace(hour=hour, minute=minute, second=0)
            dates.append(date)
    
    dates.sort()
    return dates

# Get the date range based on command line arguments
start_date, end_date = get_date_range()

# Create directory if it doesn't exist
os.makedirs(os.path.dirname(med_admin_path), exist_ok=True)

# Load existing records to avoid duplicates
existing_records, existing_med_dates = load_existing_records()

# Create medication administrations
new_records = []
medication_counts = {}
skipped_counts = {}

# Determine how many records to create based on time period
time_span = (end_date - start_date).days + 1
print(f"Time span: {time_span} days")

for med in medications:
    med_code = med["RXnormCode"]
    skipped_counts[med["Medication"]] = 0
    
    # Determine number of entries based on medication type and time span
    if args.today:
        # Today only: most medications taken once, some not at all
        if med["Medication"] in ["Simvastatin 20 MG Oral Tablet", "Clopidogrel 75 MG Oral Tablet", 
                              "24 HR metoprolol succinate 100 MG Extended Release Oral Tablet",
                              "Astemizole 10 MG Oral Tablet"]:
            # Daily medications
            entries = 1
        elif random.random() < 0.3:  # 30% chance for as-needed meds
            entries = 1
        else:
            entries = 0
    else:
        # For longer periods, scale by the time span
        if med["Medication"] in ["Simvastatin 20 MG Oral Tablet", "Clopidogrel 75 MG Oral Tablet", 
                              "24 HR metoprolol succinate 100 MG Extended Release Oral Tablet"]:
            # Daily medications - taken most but not all days
            take_probability = 0.9  # 90% of days
            entries = int(time_span * take_probability)
        elif med["Medication"] in ["Astemizole 10 MG Oral Tablet"]:
            # Regular medications
            take_probability = 0.7  # 70% of days
            entries = int(time_span * take_probability)
        elif med["Medication"] in ["Acetaminophen 300 MG / Hydrocodone Bitartrate 5 MG Oral Tablet"]:
            # As-needed medications
            take_probability = 0.2  # 20% of days
            entries = int(time_span * take_probability)
        else:
            # Occasional medications
            take_probability = 0.1  # 10% of days
            entries = int(time_span * take_probability)
    
    # Ensure at least one entry for visualization purposes if time span > 1
    if time_span > 1 and entries == 0:
        entries = 1
    
    # Track originally calculated entries
    medication_counts[med["Medication"]] = entries
    
    if entries > 0:
        # Generate potentially more dates than needed to account for possible skips
        buffer_factor = 1.5  # Generate 50% more dates than needed to compensate for skips
        dates = generate_dates(start_date, end_date, total_entries=int(entries * buffer_factor))
        
        # Keep track of successfully added entries
        successful_entries = 0
        
        for date in dates:
            # Check if this medication-date combination already exists
            date_str = date.date().isoformat()
            med_date_key = f"{med_code}:{date_str}"
            
            if med_date_key in existing_med_dates:
                # Skip this date - already have a record for this medication on this date
                skipped_counts[med["Medication"]] += 1
                continue
            
            # If we've reached our target number of entries, stop
            if successful_entries >= entries:
                break
                
            # Create medication administration entry using exactly your app's format
            med_admin_entry = {
                "resourceType": "MedicationAdministration",
                "id": str(uuid.uuid4()),
                "status": "completed",
                "medicationCodeableConcept": {
                    "coding": [
                        {
                            "system": med['RXnormSystem'] or "http://www.nlm.nih.gov/research/umls/rxnorm",
                            "code": med['RXnormCode'] or "Unknown",
                            "display": med['RXnormDisplay'] or med['Medication']
                        }
                    ],
                    "text": med["Medication"]
                },
                "subject": med["Original"]["subject"],
                "context": med["Original"]["encounter"],
                "effectiveDateTime": date.isoformat(),
                "reasonCode": med["Original"]["reasonCode"],
                "performer": [{"actor": {"display": "Patient"}}]
            }
            
            # Add to new records and track the combination to avoid duplicates
            new_records.append(med_admin_entry)
            existing_med_dates.add(med_date_key)
            successful_entries += 1
        
        # Update the count to reflect actual created entries
        medication_counts[med["Medication"]] = successful_entries

# Combine existing and new records if appending
if args.append and existing_records:
    all_records = existing_records + new_records
else:
    all_records = new_records

# Sort all records by date 
all_records.sort(key=lambda x: x["effectiveDateTime"])

# Check if the file exists, and decide to create new or append
mode = "w"  # Always write mode - we'll write all records at once
action = "Updating" if args.append else "Creating new"
print(f"{action} file: {med_admin_path}")

# Write to file
try:
    with open(med_admin_path, mode) as f:
        for record in all_records:
            f.write(json.dumps(record) + "\n")
    
    print(f"Successfully wrote {len(all_records)} medication administration records")
    print(f"- {len(new_records)} new records")
    print(f"- {len(existing_records)} existing records")
    
    print("\nNew medication distribution:")
    for med, count in medication_counts.items():
        if skipped_counts[med] > 0:
            print(f"  - {med}: {count} entries (skipped {skipped_counts[med]} duplicates)")
        else:
            print(f"  - {med}: {count} entries")
except Exception as e:
    print(f"Error writing to file: {e}")

# Print a confirmation that the file was created/updated
if os.path.exists(med_admin_path):
    size_kb = os.path.getsize(med_admin_path) / 1024
    print(f"\nFile stats: {med_admin_path}")
    print(f"File size: {size_kb:.2f} KB")
else:
    print("\nError: File was not created.")