import pandas as pd
from typing import Dict, Optional
import os

class CSVDataVerifier:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
        self.df_len = None
        self.load_data()
    
    def load_data(self):
        try:
            self.df = pd.read_csv(self.file_path)
            print(f"✅ '{self.file_path}' 로드 완료")
            print(f"📊 Size: {self.df.shape[0]} rows, {self.df.shape[1]} cols")
            self.df_len = len(self.df)
        except Exception as e:
            print(f"❌ Fail to load: {e}")
            raise
    
    def get_columns_info(self) -> Dict:
        if self.df is None:
            print("❌ NO DATA")
            return {}
        
        print("\n" + "="*50)
        print("📋 Column Information")
        print("="*50)
        
        columns_info = {}
        
        for col in self.df.columns:
            print(f"📌 {col}:")
            
            # 기본 정보
            dtype = str(self.df[col].dtype)
            null_count = self.df[col].isnull().sum()
            
            # 유일성 확인
            unique_count = self.df[col].nunique()
            is_unique = (self.df_len == unique_count)
            
            columns_info[col] = {
                'dtype': dtype,
                '# null': null_count,
                'null_percentage': (null_count / self.df_len) * 100,
                'is_unique': is_unique
            }
            
            print(f"    type: {dtype}")
            print(f"    NaN: {null_count:,} ({columns_info[col]['null_percentage']:.2f}%)")
            print(f"    uniqueness: {is_unique}")
            
            # 데이터 타입별 범위 정보
            if pd.api.types.is_numeric_dtype(self.df[col]):
                min_val = self.df[col].min()
                max_val = self.df[col].max()
                mean_val = self.df[col].mean()
                median_val = self.df[col].median()
                
                print(f"    min: {min_val}")
                print(f"    max: {max_val}")
                print(f"    mean: {mean_val:.2f}")
                print(f"    median: {median_val}")
                
                columns_info[col].update({
                    'min': min_val,
                    'max': max_val,
                    'mean': mean_val,
                    'median': median_val
                })
            
            elif pd.api.types.is_datetime64_any_dtype(self.df[col]):
                min_date = self.df[col].min()
                max_date = self.df[col].max()
                
                print(f"    min_date: {min_date}")
                print(f"    max_date: {max_date}")
                
                columns_info[col].update({
                    'min_date': min_date,
                    'max_date': max_date
                })
            
            print()
        
        return columns_info
    
    def check_column_sorting(self, column_name: str) -> Optional[Dict]:
        if self.df is None:
            print("❌ NO DATA")
            return None
        
        if column_name not in self.df.columns:
            print(f"❌ Column not found '{column_name}'")
            print(f"Column lists: {list(self.df.columns)}")
            return None
        
        print(f"\n" + "="*50)
        print(f"📊 Column '{column_name}' sorting?")
        print("="*50)
        
        is_ascending = True
        is_descending = True
        
        for i in range(1, len(self.df)):
            prev_val = self.df[column_name].iloc[i-1]
            curr_val = self.df[column_name].iloc[i]
            
            if pd.isna(prev_val) or pd.isna(curr_val):
                continue
            
            if prev_val > curr_val:
                is_ascending = False
            elif prev_val < curr_val:
                is_descending = False
            
            if not is_ascending and not is_descending:
                break
        
        if is_ascending and is_descending:
            print(f"✅ EQUAL")
            sorting_status = "all_same"
        elif is_ascending:
            print(f"✅ ASCENDING")
            sorting_status = "ascending"
        elif is_descending:
            print(f"✅ DESCENDING")
            sorting_status = "descending"
        else:
            print(f"❌ NOT SORTED")
            sorting_status = "not_sorted"
        
        if sorting_status == "not_sorted":
            for i in range(1, len(self.df)):
                prev_val = self.df[column_name].iloc[i-1]
                curr_val = self.df[column_name].iloc[i]
                
                if pd.isna(prev_val) or pd.isna(curr_val):
                    continue
                
                if prev_val > curr_val:
                    print(f"   sort break point: 행 {i+1} (인덱스 {i})")
                    print(f"     prev: {prev_val}")
                    print(f"     current: {curr_val}")
                    break
        
        return {
            'column': column_name,
            'sorting_status': sorting_status,
            'is_ascending': is_ascending,
            'is_descending': is_descending
        }
    
    def run_full_verification(self):
        print("🚀 Start CSV Data Verification...")
        
        # 통합된 컬럼 정보 확인 (유일성 및 범위 포함)
        columns_info = self.get_columns_info()
        
        print("\n" + "="*50)
        print("✅ Done!")
        print("="*50)
        
        return {
            'columns_info': columns_info
        }

def main():
    print("CSV Data Verification Tools")
    print("="*50)
    
    file_path = input("CSV path: ").strip()
    
    if not os.path.exists(file_path):
        print(f"❌ File: '{file_path}' not found")
        return
    
    try:
        verifier = CSVDataVerifier(file_path)
        verification_results = verifier.run_full_verification()
        
        while True:
            print("\n" + "-"*50)
            column_to_check = input("Check Sorted Columns ('q' to quit): ").strip()
            
            if column_to_check.lower() == 'q':
                break
            
            verifier.check_column_sorting(column_to_check)
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()