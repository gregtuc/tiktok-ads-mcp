import asyncio
import os
import json
import logging
import sys
from datetime import datetime

# Set credentials programmatically (using previously provided credentials)
os.environ["TIKTOK_APP_ID"] = "7522384699973435408"
os.environ["TIKTOK_SECRET"] = "176f78659a3be8f214ff6b5213a85c1b6341e7ed"
os.environ["TIKTOK_ACCESS_TOKEN"] = "903849518ff0d0d75b4247f3624f6d898632e635"
ADVERTISER_ID = "7441431575776526337"

# Import client and tools
from tiktok_ads_mcp.client import TikTokAdsClient
from tiktok_ads_mcp.tools.reports import get_reports

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    print("--- Analyzing TikTok Ads Performance (June 2025) ---")
    
    try:
        client = TikTokAdsClient()
        
        # Define parameters
        start_date = "2025-06-01"
        end_date = "2025-06-30"
        metrics = [
            "spend", 
            "impressions", 
            "clicks", 
            "ctr", 
            "cpc", 
            "cpm", 
            "conversion", 
            "cost_per_conversion"
        ]
        
        print(f"Fetching report for {start_date} to {end_date}...")
        
        # Fetch report grouped by campaign
        report = await get_reports(
            client,
            advertiser_id=ADVERTISER_ID,
            report_type="BASIC",
            data_level="AUCTION_CAMPAIGN",
            dimensions=["campaign_id"],
            metrics=metrics,
            start_date=start_date,
            end_date=end_date,
            page_size=100
        )
        
        print(f"\n✅ Report Fetched Successfully")
        
        # Display Total Metrics
        if report.get("total_metrics"):
            print("\n--- Total Performance (June 2025) ---")
            totals = report["total_metrics"]
            print(f"Spend: ${float(totals.get('spend', 0)):.2f}")
            print(f"Impressions: {totals.get('impressions', 0)}")
            print(f"Clicks: {totals.get('clicks', 0)}")
            print(f"Conversions: {totals.get('conversion', 0)}")
            print(f"CTR: {float(totals.get('ctr', 0)) * 100:.2f}%")
            print(f"CPC: ${float(totals.get('cpc', 0)):.2f}")
            print(f"CPA: ${float(totals.get('cost_per_conversion', 0)):.2f}")
        else:
            print("\n--- Total Performance (June 2025) ---")
            print("No total metrics available.")
        
        # Display Campaign Breakdown
        print("\n--- Campaign Breakdown ---")
        campaigns = report.get("list", [])
        if not campaigns:
            print("No campaigns found for this period.")
        
        for item in campaigns:
            dims = item.get("dimensions", {})
            mets = item.get("metrics", {})
            
            name = dims.get("campaign_id", "Unknown") # Name not available in basic report dimensions
            spend = float(mets.get("spend", 0))
            conv = int(mets.get("conversion", 0))
            cpa = float(mets.get("cost_per_conversion", 0))
            
            print(f"\nCampaign: {name}")
            print(f"  Spend: ${spend:.2f}")
            print(f"  Conversions: {conv}")
            print(f"  CPA: ${cpa:.2f}")
            print(f"  Clicks: {mets.get('clicks')}")
            print(f"  Impressions: {mets.get('impressions')}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        # import traceback
        # traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
