#!/usr/bin/env python3
"""Script to clean up admins and set the Super Admin"""

from models import storage
from models.user import User

def execute_cleanup():
    print("Starting database cleanup...")
    
    # ✅ FIX: Removed .values() because your storage engine returns a list
    all_users = storage.all(User)
    
    deleted_count = 0
    target_email = "masterbright02@gmail.com"
    master_admin = None

    for user in all_users:
        # Check if the user has admin privileges
        if getattr(user, 'is_admin', False) in [True, 1, '1', 'true', 'True']:
            
            if user.email == target_email:
                print(f"🛡️ Retaining Master Admin: {user.email}")
                master_admin = user
            else:
                print(f"🗑️ Deleting rogue admin: {user.email}")
                storage.delete(user)
                deleted_count += 1

    # Save the deletions to the database
    storage.save()
    print(f"✅ Cleanup complete! Deleted {deleted_count} old admin account(s).")

    # Upgrade the master admin to Super Admin for the new architecture
    if master_admin:
        # We use setattr to dynamically add the flag if the DB column isn't fully migrated yet
        setattr(master_admin, 'is_super_admin', True)
        storage.save()
        print(f"👑 Successfully upgraded {target_email} to SUPER ADMIN.")
    else:
        print(f"⚠️ Warning: {target_email} was not found in the database!")

if __name__ == "__main__":
    execute_cleanup()