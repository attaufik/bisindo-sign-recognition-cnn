import os
import hashlib
import argparse

def get_file_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def audit(root_dir):
    hashes = {}
    duplicates = 0
    print(f"Memulai audit dataset di folder: {root_dir}...")
    
    for split in ['train', 'val']:
        split_dir = os.path.join(root_dir, split)
        if not os.path.exists(split_dir): 
            continue
        
        for class_name in os.listdir(split_dir):
            class_dir = os.path.join(split_dir, class_name)
            if not os.path.isdir(class_dir): 
                continue
            
            for filename in os.listdir(class_dir):
                filepath = os.path.join(class_dir, filename)
                file_hash = get_file_hash(filepath)
                
                if file_hash in hashes:
                    print(f"DUPLIKAT (BOCOR/KONFLIK): {filepath} dihapus karena sama dengan {hashes[file_hash]}")
                    os.remove(filepath)
                    duplicates += 1
                else:
                    hashes[file_hash] = filepath
                    
    print(f"Audit selesai. {duplicates} gambar duplikat/bocor berhasil dihapus.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=str, default='images')
    args = parser.parse_args()
    audit(args.root)