"""
Example export service using SQLAlchemy Core for Node table queries.

This demonstrates how to:
- Query Node-owned tables
- Stream large datasets
- Generate exports without Django ORM
"""

import io
import csv
from datetime import datetime
from typing import Dict, Any
from sqlalchemy import select, and_, or_, func

from core.db import get_connection, get_table, stream_query
from services.s3 import S3Service


class ExportService:
    """
    Service for generating data exports from PostgreSQL.
    Uses SQLAlchemy Core to query Node-owned tables.
    """
    
    def __init__(self):
        self.s3_service = S3Service()
    
    def export_users_to_csv(self, filters: Dict[str, Any] = None) -> str:
        """
        Export users table to CSV and upload to S3.
        
        Args:
            filters: Optional filters like {'active': True, 'created_after': '2024-01-01'}
            
        Returns:
            S3 URL of the generated file
        """
        # Get the users table (reflected from database)
        users_table = get_table('users')
        
        # Build query
        stmt = select(users_table)
        
        if filters:
            conditions = []
            if 'active' in filters:
                conditions.append(users_table.c.active == filters['active'])
            if 'created_after' in filters:
                conditions.append(users_table.c.created_at >= filters['created_after'])
            
            if conditions:
                stmt = stmt.where(and_(*conditions))
        
        # Stream results and write to CSV
        output = io.StringIO()
        writer = None
        row_count = 0
        
        with get_connection() as conn:
            # Stream query to avoid loading all rows in memory
            for batch in stream_query(conn, stmt, batch_size=5000):
                for row_dict in batch:
                    if writer is None:
                        # Initialize CSV writer with column names from first row
                        writer = csv.DictWriter(output, fieldnames=row_dict.keys())
                        writer.writeheader()
                    
                    writer.writerow(row_dict)
                    row_count += 1
        
        # Upload to S3
        filename = f"users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        csv_bytes = output.getvalue().encode('utf-8')
        s3_url = self.s3_service.upload_file(csv_bytes, filename)
        
        return {
            'url': s3_url,
            'filename': filename,
            'row_count': row_count
        }
    
    def export_transactions(self, user_id: str = None, start_date: str = None) -> str:
        """
        Export transactions table with optional filters.
        
        Args:
            user_id: Optional user ID filter
            start_date: Optional start date filter
            
        Returns:
            S3 URL of the generated file
        """
        transactions_table = get_table('transactions')
        
        # Build query with joins if needed
        stmt = select(transactions_table)
        
        conditions = []
        if user_id:
            conditions.append(transactions_table.c.user_id == user_id)
        if start_date:
            conditions.append(transactions_table.c.created_at >= start_date)
        
        if conditions:
            stmt = stmt.where(and_(*conditions))
        
        # Order by created_at for consistent exports
        stmt = stmt.order_by(transactions_table.c.created_at.desc())
        
        # Stream and export
        output = io.StringIO()
        writer = None
        row_count = 0
        
        with get_connection() as conn:
            for batch in stream_query(conn, stmt, batch_size=10000):
                for row_dict in batch:
                    if writer is None:
                        writer = csv.DictWriter(output, fieldnames=row_dict.keys())
                        writer.writeheader()
                    
                    writer.writerow(row_dict)
                    row_count += 1
        
        # Upload
        filename = f"transactions_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        csv_bytes = output.getvalue().encode('utf-8')
        s3_url = self.s3_service.upload_file(csv_bytes, filename)
        
        return {
            'url': s3_url,
            'filename': filename,
            'row_count': row_count
        }
    
    def get_user_stats(self) -> Dict[str, Any]:
        """
        Get aggregated user statistics using SQLAlchemy Core.
        
        Returns:
            Dictionary with user stats
        """
        users_table = get_table('users')
        
        with get_connection() as conn:
            # Total users
            total_stmt = select(func.count()).select_from(users_table)
            total_users = conn.execute(total_stmt).scalar()
            
            # Active users
            active_stmt = select(func.count()).select_from(users_table).where(
                users_table.c.active == True
            )
            active_users = conn.execute(active_stmt).scalar()
            
            return {
                'total_users': total_users,
                'active_users': active_users,
                'inactive_users': total_users - active_users
            }
