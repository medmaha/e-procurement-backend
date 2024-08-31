from decimal import Decimal
import math
from django.db import models
from apps.procurement.models.rfq import RFQ, RFQItem
from apps.vendors.models.rfq_response import RFQResponse
from apps.organization.models.staff import Staff
from apps.core.utilities.text_choices import ApprovalChoices
from typing import List, Sequence


class RFQQuotationEvaluation(models.Model):
    quotation = models.ForeignKey(
        RFQResponse, on_delete=models.CASCADE, related_name="evaluation"
    )
    item = models.ForeignKey(
        RFQItem, on_delete=models.CASCADE, related_name="evaluations"
    )
    quantity = models.IntegerField(default=1)
    pricing = models.DecimalField(max_digits=10, decimal_places=2)
    comments = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=1)
    status = models.CharField(max_length=100, default="pending")
    specifications = models.BooleanField(default=False)

    officer = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "RFQ Response Evaluation"
        constraints = [
            models.constraints.UniqueConstraint(
                name="unique_evaluation",
                fields=["quotation", "item"],
                violation_error_message="This quotation and item has already been evaluated.",
            )
        ]

    def __str__(self):
        return f"Evaluation - {self.quotation} - {self.item}"


class RFQEvaluation(models.Model):
    rfq = models.OneToOneField(RFQ, on_delete=models.CASCADE, related_name="evaluation")
    evaluations = models.ManyToManyField(
        RFQQuotationEvaluation, related_name="evaluation"
    )
    officer = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Evaluation - {self.rfq}"

    class Meta:
        verbose_name = "RFQ Evaluation"

    from typing import List

    def determine_winner(self, evaluations=None) -> dict:
        """
        This function determines the best winner from the evaluations array
        """

        from apps.procurement.api.serializers.rfq_evaluation import (
            RFQQuotationWinnerEvaluationSerializer,
        )

        rfq_evaluation = self

        # Get all evaluations associated with the RFQEvaluation
        evaluations = evaluations or rfq_evaluation.evaluations.filter()

        # Filter evaluations by status (e.g., only consider completed evaluations)
        completed_evaluations = [
            evaluation
            for evaluation in evaluations
            if evaluation.status.lower() == "submitted"
        ]

        if not completed_evaluations:
            # If there are no completed evaluations, return an empty dict
            return {}

        # Group evaluations by vendor
        vendor_evaluations = {}
        winners_list = []
        winners = {}
        for evaluation in completed_evaluations:
            vendor_name = evaluation.quotation.vendor.name

            if vendor_name not in vendor_evaluations:
                vendor_evaluations[vendor_name] = {
                    "total_pricing": 0,
                    "total_rating": 0,
                    "total_specs": 0,
                    "total_quantity": 0,
                    "evaluations": [],
                    "rfq_id": evaluation.quotation.rfq.pk,
                    "rfq_response_id": evaluation.quotation.pk,
                }
            vendor_evaluations[vendor_name]["total_pricing"] += evaluation.pricing
            vendor_evaluations[vendor_name]["total_rating"] += evaluation.rating
            vendor_evaluations[vendor_name]["total_specs"] += evaluation.specifications
            vendor_evaluations[vendor_name]["total_quantity"] += evaluation.quantity
            vendor_evaluations[vendor_name]["evaluations"].append(
                RFQQuotationWinnerEvaluationSerializer(
                    evaluation, context={"slim": True}
                ).data
            )

            serialized_data = vendor_evaluations[vendor_name]
            # for vendor_name, serialized_data in vendor_evaluations.items():
            evaluation_count = len(serialized_data["evaluations"])
            total_pricing = serialized_data["total_pricing"]
            total_rating = serialized_data["total_rating"]
            total_specs = serialized_data["total_specs"]
            total_quantity = serialized_data["total_quantity"]

            # Determining the winner based on the average pricing, average rating, and total specifications
            average_pricing = total_pricing / evaluation_count
            average_rating = total_rating / evaluation_count
            average_specs = total_specs / evaluation_count
            average_quantity = total_quantity / evaluation_count

            winner_criteria = {
                "average_pricing": int(total_pricing / evaluation_count),
                "average_rating": int(total_rating / evaluation_count),
                "total_specs": total_specs,
            }
            factor_score = (
                float(average_pricing),
                float(average_rating),
                float(average_specs),
                float(average_quantity),
            )

            winner_data = {
                "factor_score": factor_score,
                "winner_criteria": winner_criteria,
                **serialized_data,
            }

            winners[vendor_name] = winner_data
            winners_list.append({"vendor_name": vendor_name, **winner_data})

        best_winner = min(winners_list, key=lambda x: x["factor_score"])
        winner = winners.get(best_winner["vendor_name"], {})
        return {best_winner["vendor_name"]: winner}


class RFQEvaluationApprover(models.Model):
    evaluation = models.ForeignKey(
        RFQEvaluation, on_delete=models.CASCADE, related_name="approval_record"
    )
    officer = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    approve = models.CharField(max_length=100, choices=ApprovalChoices.choices)

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Approval - {self.evaluation}"
